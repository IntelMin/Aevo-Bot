
import { BigNumber } from "bignumber.js";
BigNumber.config({EXPONENTIAL_AT: 1e+9});

export const notNill = (value) => {
	return !!value
}

export const truncateAddress = (address, first = 5, last = 5) => {
	address.slice(0, first) + '...' + address.slice(-last, address.length)
}

export const truncateString = (text, max = 256) => {
	if (text.length > max) return text.substring(0, max) + ' ...'
	return text
}

export const bigMul = (num1, num2) => {
	return new BigNumber(num1).multipliedBy(num2).toString();
}

export const BntoNum = (value, decimal = 18) => {
  return new BigNumber(value).shiftedBy(-decimal).toNumber();
}

export const NumToBn = (value, decimal = 18) => {
  return new BigNumber(value).shiftedBy(decimal);
}