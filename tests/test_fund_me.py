from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = 0xA7F408a227Fffd7Cbc4B65578476029B219AA16d
    # code below should pass and do exception for "bad_actor" not being the owneraddress which is 
    # the only address allowed to make withdrawals. the fund_me.withdraw({"from": bad_actor}) function is not parsing correctly for some 
    # reason and is giving this error: FAILED tests/test_fund_me.py::test_only_owner_can_withdraw - web3.exceptions.BadResponseFormat:
    #  The response was in an unexpected format and unable to be parsed. Response cannot include both "error" and "result"
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})

# fund_me.withdraw({"from": bad_actor})   
# account = get_account() 
# with pytest.raises(exceptions.VirtualMachineError): 
# error code below is what shows up when trying to run pytest with bad_actor = accounts.add()
# is the accounts.add() function not being called correctly? parsed correctly? imported properly? Fix?
"""
response = {'error': {'code': -32000, 'data': {'0x62cb651a36a1ad4469fc68b57794602455e33aa67c28b9cdad0a940326440ee2': {'error': 'r...: revert'}, 'id': 38, 'jsonrpc': '2.0', 'result': '0x62cb651a36a1ad4469fc68b57794602455e33aa67c28b9cdad0a940326440ee2'}
error = 'Response cannot include both "error" and "result"'

    def _raise_bad_response_format(response: RPCResponse, error: str = "") -> None:
        message = "The response was in an unexpected format and unable to be parsed."
        raw_response = f"The raw response is: {response}"

        if error is not None and error != "":
            message = f"{message} {error}. {raw_response}"
        else:
            message = f"{message} {raw_response}"

>       raise BadResponseFormat(message)
""" 
