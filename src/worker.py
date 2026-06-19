import asyncio
import os

from entrypoints.worker import main

if __name__ == "__main__":
    print(f'{os.getenv("MISTRAL_API_KEY")=}')
    asyncio.run(main())
