# **Buscador de Palavras em PDFs**  

## 📌 **Descrição**  
O **Buscador de Palavras em PDFs** é um aplicativo eficiente que permite localizar palavras-chave dentro de arquivos PDF em uma pasta predefinida. Ideal para profissionais que lidam com grandes volumes de documentos, o aplicativo exibe os arquivos e as páginas onde a palavra foi encontrada, permitindo uma navegação rápida e precisa.  

---

## 🚀 **Funcionalidades**  
- 🔎 **Busca rápida e eficiente** em todos os PDFs da pasta configurada.  
- 📄 **Exibição detalhada** dos arquivos e páginas onde a palavra aparece.  
- 📂 **Pasta pré-configurada**, com opção de alteração mediante senha.  
- 🔓 **Proteção por senha** para mudança da pasta de busca.  
- 📖 **Abertura direta do PDF** na página encontrada (Adobe Acrobat ou navegador).  
- 📊 **Barra de progresso** para acompanhamento da busca.  
- ✅ **Interface simples e intuitiva** para facilitar a usabilidade.  

---

## 🛠️ **Instalação e Execução**  

### **Pré-requisitos:**  
Antes de executar o aplicativo, instale os seguintes pacotes:  

```bash
pip install pymupdf PyQt5
```

### **Execução:**  
Para iniciar o programa, execute o seguinte comando no terminal:  

```bash
python buscador_pdfs.py
```
## 🔹 **Como Transformar o Aplicativo em um Executável com Ícone**  

Se você deseja converter seu script Python em um executável (.exe) para rodar sem precisar do interpretador Python instalado, siga este tutorial passo a passo.  

---

### **1️⃣ Instalar o PyInstaller**  
O **PyInstaller** é uma ferramenta que permite empacotar o código Python em um executável. Para instalá-lo, abra o terminal (cmd, PowerShell ou terminal do VS Code) e digite:  

```bash
pip install pyinstaller
```

---

### **2️⃣ Criar o Executável**  
Após instalar o `pyinstaller`, vá até a pasta onde está seu script (`buscador_pdfs.py`) e execute o seguinte comando:  

```bash
pyinstaller --onefile --windowed --icon=logoempresa.ico buscador_pdfs.py
```

🔹 **Explicação dos parâmetros:**  
- `--onefile` → Gera um único arquivo `.exe`, em vez de várias pastas.  
- `--windowed` → Evita que um terminal do console abra junto ao programa.  
- `--icon=logoempresa.ico` → Define um ícone personalizado para o executável.  

⚠️ **Atenção:** O ícone precisa estar no formato `.ico`. Se sua imagem estiver em `.png` ou `.jpg`, converta para `.ico` usando sites como [icoconvert.com](https://icoconvert.com/).  

---

### **3️⃣ Localizar o Executável**  
Depois de rodar o comando, o executável estará dentro da pasta **`dist/`** no mesmo diretório do seu script.  

📂 Estrutura após a criação:  
```
📁 projeto/
  ├── 📁 build/
  ├── 📁 dist/
  │     ├── 📄 buscador_pdfs.exe  ✅ (Executável gerado)
  ├── 📄 buscador_pdfs.spec
  ├── 📄 buscador_pdfs.py
  ├── 📄 logoempresa.ico
```

---

### **4️⃣ Testar o Executável**  
Agora, vá até a pasta `dist/` e execute `buscador_pdfs.exe` para testar se está funcionando corretamente.  

---

### **5️⃣ Opcional: Compactar e Distribuir**  
Se quiser distribuir seu programa, pode compactar a pasta `dist/` em um `.zip` e compartilhar o arquivo `.exe` com outras pessoas.  

---

## ⚙️ **Configuração da Pasta Padrão**  
- O aplicativo inicia com uma pasta predefinida para buscas.  
- Para alterar a pasta, clique no botão **"Alterar Pasta"** e insira a senha correta (`darash6`).  

---

## 📌 **Como Usar**  
1. **Digite a palavra-chave** desejada no campo de pesquisa.  
2. **Clique no botão "Buscar nos PDFs"** para iniciar a pesquisa.  
3. Aguarde a barra de progresso carregar.  
4. Os arquivos encontrados aparecerão na lista.  
5. **Clique em um arquivo** para abri-lo diretamente na página correta.  

---

## 🔑 **Alteração da Pasta**  
- Para alterar a pasta padrão, clique no botão **"Alterar Pasta"**.  
- Digite a senha: **darash6**.  
- Escolha a nova pasta e confirme.  

---

## 🖥️ **Compatibilidade**  
- **Sistema Operacional:** Windows 10/11  
- **Leitor de PDFs:** Adobe Acrobat (recomendado) ou navegador  

---

## 📜 Licença  

Este projeto é distribuído sob a Licença MIT.  

Você pode usá-lo, modificá-lo e distribuí-lo livremente, desde que mantenha a atribuição ao autor original:  

**Desenvolvido por darash6**.  



---

💡 **Desenvolvido para facilitar a busca em arquivos PDF de maneira rápida e eficiente!** 🚀
