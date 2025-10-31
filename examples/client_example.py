"""Beispiel-Client für MCP Server."""

import asyncio
import httpx


async def example_list_models():
    """Beispiel: Modelle auflisten."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:4838/mcp/tools/call",
            json={
                "name": "ollama_list_models",
                "arguments": {},
            },
        )
        print("Modelle:")
        print(response.json())


async def example_generate():
    """Beispiel: Text generieren."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:4838/mcp/tools/call",
            json={
                "name": "ollama_generate",
                "arguments": {
                    "model": "llama2",
                    "prompt": "Erkläre mir Python in einem Satz.",
                },
            },
            timeout=60.0,
        )
        result = response.json()
        print("Generierte Antwort:")
        print(result.get("result", {}).get("response", ""))


async def example_chat():
    """Beispiel: Chat."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:4838/mcp/tools/call",
            json={
                "name": "ollama_chat",
                "arguments": {
                    "model": "llama2",
                    "messages": [
                        {"role": "user", "content": "Hallo! Wie geht es dir?"}
                    ],
                },
            },
            timeout=60.0,
        )
        result = response.json()
        print("Chat-Antwort:")
        if result.get("result", {}).get("message"):
            print(result["result"]["message"].get("content", ""))


async def example_health_check():
    """Beispiel: Health-Check."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:4838/health")
        print("Health-Status:")
        print(response.json())


async def main():
    """Hauptfunktion."""
    print("=== MCP Server Client Beispiele ===\n")

    # Health-Check
    print("1. Health-Check:")
    try:
        await example_health_check()
    except Exception as e:
        print(f"Fehler: {e}")
    print()

    # Modelle auflisten
    print("2. Modelle auflisten:")
    try:
        await example_list_models()
    except Exception as e:
        print(f"Fehler: {e}")
    print()

    # Text generieren (kommentiert, da es länger dauern kann)
    # print("3. Text generieren:")
    # try:
    #     await example_generate()
    # except Exception as e:
    #     print(f"Fehler: {e}")
    # print()

    # Chat (kommentiert, da es länger dauern kann)
    # print("4. Chat:")
    # try:
    #     await example_chat()
    # except Exception as e:
    #     print(f"Fehler: {e}")


if __name__ == "__main__":
    asyncio.run(main())

