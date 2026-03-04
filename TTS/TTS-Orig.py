import asyncio
import edge_tts

async def main():
    tts = edge_tts.Communicate(
        "Olá, isso é um teste de voz.",
        voice="pt-BR-AntonioNeural"
    )
    await tts.save("D:\Videos\\n8n\\audio1.mp3")

asyncio.run(main())