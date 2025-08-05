# 🎮 GameAvi – Your AI-Powered Gaming Companion

GameAvi is an intelligent, real-time **GenAI-based gaming assistant** that helps players strategize, optimize builds, and navigate complex quests in their favorite games. It dynamically adapts to your playstyle and gameplay data to offer personalized suggestions using state-of-the-art AI techniques like **Prompt Engineering**, **RAG (Retrieval-Augmented Generation)**, **Structured Output**, and **Function Calling**.

---

## 🚀 Features

- 🎯 **Playstyle-Aware Advice**  
  Get personalized strategy tips based on your current build, level, items, and goals.

- 📚 **RAG Integration**  
  Connects to in-game wikis, lore documents, and mod files to provide grounded, lore-accurate responses.

- ⚙️ **Function Calling (API Tool Use)**  
  Uses your real-time stats, inventory, and quest logs to tailor AI output.

- 🧾 **Structured Output**  
  Returns ready-to-use data formats for UI rendering, mod integration, or direct use in game overlays.

- 💡 **Supports Multiple Game Genres**
  - RPGs: Elden Ring, Skyrim, Witcher
  - Survival: Minecraft, Valheim
  - FPS: Valorant, Apex Legends
  - MMORPG: WoW, Genshin Impact

---

## 🧠 Core AI Concepts Used

| Concept            | Usage in GameAvi                                                                 |
|--------------------|----------------------------------------------------------------------------------|
| **Prompting**       | Smart system & user prompts tailor AI responses for gameplay scenarios           |
| **RAG**             | Retrieves lore, item stats, and map data from vector stores (e.g., FAISS, ChromaDB) |
| **Function Calling**| Connects to functions like `getPlayerStats()`, `getInventoryItems()`             |
| **Structured Output** | Outputs JSON-like data for UI components and strategy engines                   |

---

## 🛠️ Tech Stack

| Layer        | Technology                  |
|--------------|-----------------------------|
| Frontend     | React.js / Electron.js      |
| Backend      | Node.js + Express.js        |
| AI Core      | OpenAI GPT-4 / LangChain / Local LLM |
| RAG Layer    | ChromaDB / FAISS            |
| Data Sources | Game Wiki APIs / Custom Docs |
| Auth         | JWT / OAuth (optional)      |

---

## 🔧 Sample Function Calls

```js
getPlayerStats(playerId)
getInventoryItems()
getQuestLog()
getMapLocations(region)
getLoreData("Cursed King")
