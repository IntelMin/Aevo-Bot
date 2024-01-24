import { ethers } from 'ethers';
// import promisify from 'promisify';
const util = require('util')

const provider = new ethers.JsonRpcProvider('https://l2-aevo-mainnet-prod-0.t.conduit.xyz');
// const provider = new ethers.JsonRpcProvider('https://mainnet.infura.io/v3/2377373e9cc84228a6cea33645b511ea');

export async function auth(req, res) {
  try {
    console.log("[api/auth] Requested");

    const account = req.query.address;

    const signer = ethers.Wallet.createRandom();
    signer.connect(provider);

    console.log(' -- Signer -- ');
    console.log(signer.address);
    console.log(await provider.getSigner());

    // First we hash the register data
    const registerHash = ethers.TypedDataEncoder.hash(
      {
        name: "Aevo Mainnet",
        version: "1",
        chainId: 1,
      },
      {
        Register: [
          { name: "key", type: "address" },
          { name: "expiry", type: "uint256" },
        ],
      },
      {
        key: await signer.getAddress(),
        expiry: ethers.MaxUint256.toString(),
      }
    );
    
    console.log(' -- registerHash -- ');
    console.log(registerHash);


    // Then we sign the hash
    const res = await provider.provider.send("eth_sign", [account.toLowerCase(), registerHash]);
       

    // This is the account_signature
    const accountSignature = res.result;

    console.log(' -- accountSignature -- ');
    console.log(accountSignature);

    // const signingKeySignature = await signer._signTypedData(
    //   {
    //     name: "Aevo Mainnet",
    //     version: "1",
    //     chainId: 1,
    //   },
    //   {
    //     SignKey: [{ name: "account", type: "address" }],
    //   },
    //   {
    //     account: account
    //   }
    // );

    // res.status(200).json(
    //   { 
    //     signingKey: signer,
    //     accountSignature: accountSignature,
    //     signingKeySignature: signingKeySignature
    //   }
    // );
  } catch(e) {
    console.error("[api/singing_key] Error:", e);
    res.status(500).json({ error: e });
  }
}