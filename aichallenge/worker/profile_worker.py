import asyncio

async def delete_pic(file, attempt = 1):
    try:
        file.delete()
        print("file deleted successfully")
    except Exception as e:
        if attempt <= 3:
            await delete_pic(file, attempt = attempt + 1)
        else:
            print(f"Error when deleting {file.name} : {e.message}")

    