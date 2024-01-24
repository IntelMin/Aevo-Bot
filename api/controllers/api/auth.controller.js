import { ethers } from 'ethers';
// import promisify from 'promisify';
const util = require('util')

const provider = new ethers.JsonRpcProvider('https://l2-aevo-mainnet-prod-0.t.conduit.xyz');

export async function auth(req, res) {
  try {
    console.log("[api/auth] Requested");

    const account = req.body.address;
    const private_key = req.body.private_key;

    const signer  = ethers.Wallet.createRandom();
    const signerAccount = new ethers.Wallet(private_key, provider);

    // First we hash the register data
    // const registerHash = ethers.TypedDataEncoder.hash(
    //   {
    //     name: "Aevo Mainnet",
    //     version: "1",
    //     chainId: 1,
    //   },
    //   {
    //     Register: [
    //       { name: "key", type: "address" },
    //       { name: "expiry", type: "uint256" },
    //     ],
    //   },
    //   {
    //     key: await signer.getAddress(),
    //     expiry: ethers.MaxUint256.toString(),
    //   }
    // );

    // Then we sign the hash
    // const res = await provider.provider.send("eth_sign", [account.toLowerCase(), registerHash]);

    const accountSignature = await signerAccount.signTypedData(
      {
        name: "Aevo Mainnet",
        version: "1",
        chainId: 1,
      },
      {
        SignKey: [{ name: "account", type: "address" }],
      },
      {
        account: account
      }
    );

    const signingKeySignature = await signer.signTypedData(
      {
        name: "Aevo Mainnet",
        version: "1",
        chainId: 1,
      },
      {
        SignKey: [{ name: "account", type: "address" }],
      },
      {
        account: signer.address
      }
    );

    res.status(200).json(
      { 
        signingKey: signer,
        accountSignature: accountSignature,
        signingKeySignature: signingKeySignature
      }
    );

  } catch(e) {
    console.error("[api/singing_key] Error:", e);
    res.status(500).json({ error: e });
  }
}