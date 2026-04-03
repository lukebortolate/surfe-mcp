import os
import httpx
import uvicorn
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Surfe")
SURFE_API_KEY = os.environ["SURFE_API_KEY"]
BASE = "https://api.surfe.com/v2"
HEADERS = {"Authorization": f"Bearer {SURFE_API_KEY}", "Content-Type": "application/json"}

@mcp.tool()
async def cerca_persone(titolo: str, settore: str = "", paese: str = "IT", max_risultati: int = 25) -> dict:
    """Cerca persone su Surfe per titolo, settore e paese."""
    payload = {"filters": {"jobTitles": [titolo], "countries": [paese]}, "limit": max_risultati}
    if settore:
        payload["filters"]["industries"] = [settore]
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE}/people/search", headers=HEADERS, json=payload)
        return r.json()

@mcp.tool()
async def arricchisci_persona(linkedin_url: str, vuoi_email: bool = True, vuoi_mobile: bool = False) -> dict:
    """Dato un URL LinkedIn, restituisce email e/o telefono."""
    payload = {"include": {"email": vuoi_email, "mobile": vuoi_mobile}, "people": [{"linkedinUrl": linkedin_url}]}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE}/people/enrich", headers=HEADERS, json=payload)
        return r.json()

@mcp.tool()
async def cerca_aziende(settore: str, paese: str = "IT", dipendenti_min: int = 0, dipendenti_max: int = 10000, max_risultati: int = 25) -> dict:
    """Cerca aziende su Surfe per settore, paese e dimensione."""
    payload = {"filters": {"countries": [paese], "industries": [settore], "numberOfEmployees": {"min": dipendenti_min, "max": dipendenti_max}}, "limit": max_risultati}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE}/companies/search", headers=HEADERS, json=payload)
        return r.json()

@mcp.tool()
async def arricchisci_azienda(dominio: str) -> dict:
    """Dato il dominio di un'azienda, restituisce dati completi."""
    payload = {"companies": [{"domain": dominio}]}
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE}/companies/enrich", headers=HEADERS, json=payload)
        return r.json()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(mcp.get_asgi_app(), host="0.0.0.0", port=port)
