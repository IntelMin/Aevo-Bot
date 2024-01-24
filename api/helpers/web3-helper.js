import { bigMul } from './utils';
import { BigNumber } from "bignumber.js";
import { Web3 } from 'web3'
import * as constants from './constants';
import BN from 'bn.js'

export const sendTx = async (encodedABI, privateKey) => {
  const web3 = new Web3(constants.WEB3_RPC_URL);
  const account = web3.eth.accounts.privateKeyToAccount(privateKey);
  const gasPrice = await web3.eth.getGasPrice();
  const suggestedGasPrice = new BN(gasPrice.toString()).mul(new BN(1.2));
  
  const tx = {
    from: account.address,
    gas: 100000000,
    gasPrice: suggestedGasPrice.toString(),
    data: encodedABI,
  };
  
  const signedTx = await web3.eth.accounts.signTransaction(tx, privateKey);
  
  const res = await (() => new Promise((resolve, reject) => {
    const sentTx = web3.eth.sendSignedTransaction(signedTx.raw || signedTx.rawTransaction);
    sentTx.on("receipt", receipt => {
      resolve(receipt);
    });
    sentTx.on("error", err => {
      reject(err);
    });
  }))();
  
  return res;
}

export const getWeb3 = (privateKey) => {
  const web3 = new Web3(constants.WEB3_RPC_URL);
  const account = web3.eth.accounts.privateKeyToAccount(privateKey);
  web3.eth.accounts.wallet.add(account);
  web3.eth.defaultAccount = account.address;
  return web3;
}

export const getGas = async (web3, tx, options = {}) => {
  const gas = await tx.estimateGas(options);
  const gasPrice = await web3.eth.getGasPrice();
  const suggestedGas = bigMul(gas.toString(), 1.5);
  const suggestedGasPrice = bigMul(gasPrice.toString(), 1.2);
  return { gas: suggestedGas, gasPrice: suggestedGasPrice};
}

export const getDeadline = async () => {
  const web3 = new Web3(constants.WEB3_RPC_URL);
  const blockNumber = await web3.eth.getBlockNumber();
  const blockTimestamp = (await web3.eth.getBlock(blockNumber)).timestamp;
  return new BigNumber(blockTimestamp.toString()).plus(100).toString();
}