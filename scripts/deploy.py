from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS





  


# function/script below runs get_account() from helpful_scripts, we imported this function
# Were deploying our contract from the account that we got from get_account()
# Were going to verify that the source code was published with publish source=True
# then well print out the address where the contract was deployed to 

def deploy_fund_me():
    account = get_account()
    print("got account...") 
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS: 
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    fund_me = FundMe.deploy(
        price_feed_address, 
        {"from":account}) 
    #publish_source=config["networks"][network.show_active()].get("verify")
    # pass the price feed address to our fundme contract 
    # if we are on a persistent network like sepolia, use the associated address
    # otherwise, use/deploy mocks
    # used variable LOCAL_BLOCKCHAIN_ENVIRONMENTS for our developement chains.
    # should have, publish_source=True, after {"from": account} in FundMe.deploy to publish/verify
    # source code on Etherscan 
    # Etherscan API not working for some reason. Indexing error? space in home path? will resolve/look into more down the road. 
    print(f"FundMe contract deployed to: {fund_me.address}")
    return fund_me

def main():
    deploy_fund_me()



    