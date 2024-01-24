import { ethers } from "ethers";
// import promisify from 'promisify';
const util = require("util");

const provider = new ethers.JsonRpcProvider(
  "https://l2-aevo-mainnet-prod-0.t.conduit.xyz"
);

export async function auth(req, res) {
  try {
    console.log("[api/auth] Requested");

    const { account, private_key } = req.body;

    const signer = ethers.Wallet.createRandom();
    const signerAccount = new ethers.Wallet(private_key, provider);

    const accountSignature = await signerAccount.signTypedData(
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
        account: account,
      }
    );

    res.status(200).json({
      signer_address: signer.address,
      account_signature: accountSignature,
      signing_key_signature: signingKeySignature,
    });
  } catch (e) {
    console.error("[api/singing_key] Error:", e);
    res.status(500).json({ error: e });
  }
}
