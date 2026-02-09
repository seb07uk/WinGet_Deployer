

# <h1 align="center">WinGet Deployer v2.1</h1>

An advanced GUI-based package management utility designed for Windows, leveraging the power of the **Microsoft WinGet** engine. This tool provides a streamlined interface for IT professionals to search, install, upgrade, and manage system software with enhanced visual feedback.

## 🚀 Key Features

* **Real-time Interaction**: Execute WinGet commands through an intuitive dashboard.
* **Smart Highlighting**: 
    * **Neon Green**: Exact matches for searched Package IDs.
    * **Yellow**: Related software and dependencies found in the results.
* **Productivity Focused**: 
    * **Auto-completion**: Suggestions for popular packages (Chrome, VS Code, Git, etc.).
    * **Context Actions**: Right-click any text in the console to instantly copy it to the search bar.
    * **Hotkey Support**: Press `Enter` to trigger a search immediately.
* **Visual Customization**: Toggle between **Dark Mode** and **Light Mode** with high-contrast UI elements.
* **Dual Language**: Seamlessly switch between English and Polish.

## 📂 System Paths & Storage

The application adheres to the `polsoft.ITS™` environment standards. All configurations and temporary files are stored in the following directory:

* **Settings**: `%userprofile%\.polsoft\WinGet\settings.json`
* **Repair Cache**: `%userprofile%\Downloads\WinGet\`

## 🛠 Installation & Requirements

1.  **Operating System**: Windows 10 or Windows 11.
2.  **Engine**: WinGet CLI must be installed (if missing, use the built-in "Repair/Install WinGet" button).
3.  **Python Dependencies** (if running from source):
    ```bash
    pip install tkinter
    ```

## 📦 Compilation to EXE

To build a standalone executable with the polsoft branding:
1. Ensure `icon.ico` and `version.txt` are in the root directory.
2. Run the provided `build.bat` script.
3. The resulting EXE will be located in the `\dist` folder, configured with no-console mode and full version metadata.

---

# <h1 align="center">WinGet Deployer v2.1 (PL)</h1>

Zaawansowane narzędzie GUI do zarządzania pakietami w systemie Windows, wykorzystujące silnik **Microsoft WinGet**. Aplikacja oferuje zoptymalizowany interfejs dla profesjonalistów IT, umożliwiając szybkie wyszukiwanie, instalację i aktualizację oprogramowania z zaawansowanym systemem wizualnego wsparcia.

## 🚀 Kluczowe Funkcje

* **Interakcja w Czasie Rzeczywistym**: Wykonywanie komend WinGet przez intuicyjny panel.
* **Inteligentne Podświetlanie**: 
    * **Neonowa Zieleń**: Dokładne dopasowania wyszukiwanego ID pakietu.
    * **Żółty**: Powiązane programy i zależności widoczne w wynikach.
* **Zorientowanie na Produktywność**: 
    * **Auto-uzupełnianie**: Sugestie dla popularnych pakietów (Chrome, VS Code, Git itp.).
    * **Akcje Kontekstowe**: Kliknięcie prawym przyciskiem myszy na tekst w konsoli kopiuje go bezpośrednio do pola wyszukiwania.
    * **Obsługa Enter**: Szybkie uruchamianie wyszukiwania klawiszem Enter.
* **Personalizacja Wizualna**: Przełącznik między trybem Ciemnym (**Dark**) i Jasnym (**Light**).
* **Wielojęzyczność**: Pełne wsparcie dla języka Polskiego i Angielskiego.

## 📂 Ścieżki Systemowe i Przechowywanie

Aplikacja działa zgodnie ze standardami środowiska `polsoft.ITS™`. Wszystkie konfiguracje są przechowywane w:

* **Ustawienia**: `%userprofile%\.polsoft\WinGet\settings.json`
* **Cache Naprawy**: `%userprofile%\Downloads\WinGet\`

## 🛠 Wymagania i Instalacja

1.  **System**: Windows 10 lub Windows 11.
2.  **Silnik**: Wymagany WinGet CLI (w przypadku braku, użyj funkcji "Napraw / Instaluj WinGet").
3.  **Zależności Python** (przy uruchamianiu ze źródeł):
    ```bash
    pip install tkinter
    ```

## 📦 Kompilacja do EXE

Aby utworzyć samodzielny plik wykonywalny:
1. Upewnij się, że plik `icon.ico` oraz `version.txt` znajdują się w folderze głównym.
2. Uruchom skrypt `build.bat`.
3. Gotowy plik EXE znajdzie się w folderze `\dist` (skonfigurowany bez okna konsoli i z pełnymi metadanymi wersji).

---
<h6 align="center">© 2026 polsoft.ITS™ London by Sebastian Januchowski</h6>
