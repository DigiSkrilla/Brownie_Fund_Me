//SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

import "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";

// import "@chainlink/contracts/src/v0.8/vendor/SafeMathChainlink.sol"; this is old code no longer needed. Safemath for gas is abstracted into the background
// import {AggregatorV3Interface} from "@chainlink/contracts@1.2.0/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";
// import statement above is same as interface code below this line
// pasted code in to see exactly whats going on. The code below allows you to use functions from the chainlink interface.
/*
interface AggregatorV3Interface {
    function decimals() external view returns (uint8);

    function description() external view returns (string memory);

    function version() external view returns (uint256);

    function getRoundData(
        uint80 _roundId
    )
        external
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );

    function latestRoundData()
        external
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );
}
*/
contract FundMe {
    //  using SafeMathChainlink for uint256;
    // code above checks math for versions less than 0.8.0. Checks for proper unit conversion im pretty sure.
    // but don't have to worry with 0.8 and above.

    // mapping is like creating an array or dictionary, but its immutable and cant be iterated through.
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;

    // declaring the variable for the owner address.
    address public owner;

    AggregatorV3Interface public priceFeed;

    // constructors are kind of like functions, but the code in them gets ran prior to all other functions
    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        // $50
        uint256 minimumUSD = 50 * 10 ** 18;
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
        // need to know what the conversion rate is from ETH => USD...Chainlink
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConversionRate(
        uint256 ethAmount
    ) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = ((ethPrice * ethAmount) / 10 ** 18);
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10 ** 18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10 ** 18;
        return (minimumUSD * precision) / price;
    }

    // modifiers allow you to attach some code/modify a function with a keyword.
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        (bool success, ) = msg.sender.call{value: address(this).balance}("");
        require(success);

        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }
}
