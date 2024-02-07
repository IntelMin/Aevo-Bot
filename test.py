from aevo.sign_up import sign_up

async def main():
    await sign_up('0xcfd92db493a727a5142b3a28ba392ba0b942955de38e3180e3945b691bd892d5')

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())