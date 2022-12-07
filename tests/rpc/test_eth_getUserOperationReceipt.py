import pytest
import json
from jsonschema import validate, Validator

from tests.types import RPCRequest
from tests.utils import userOpHash, assertRpcError
from .test_eth_sendUserOperation import sendUserOperation


@pytest.mark.usefixtures('sendUserOperation')
@pytest.mark.parametrize('method', ['eth_getUserOperationReceipt'], ids=[''])
def test_eth_getUserOperationReceipt(cmd_args, wallet_contract, userOp, w3, schema):
    response = RPCRequest(method="eth_getUserOperationReceipt",
                          params=[userOpHash(wallet_contract, userOp)]).send(cmd_args.url)
    assert response.result['userOpHash'] == userOpHash(wallet_contract, userOp)
    receipt = w3.eth.getTransactionReceipt(response.result['receipt']['transactionHash'])
    assert response.result['receipt']['blockHash'] == receipt['blockHash'].hex()
    Validator.check_schema(schema)
    validate(instance=response.result, schema=schema)


def test_eth_getUserOperationReceipt_error(cmd_args):
    response = RPCRequest(method="eth_getUserOperationReceipt", params=['']).send(cmd_args.url)
    assertRpcError(response, 'Missing/invalid userOpHash', -32601)