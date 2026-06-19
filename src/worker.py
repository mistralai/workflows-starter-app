import asyncio
import os

from entrypoints.worker import main

if __name__ == "__main__":
    print(f'{os.getenv("MISTRALAI_API_KEY")=}')
    asyncio.run(main())
