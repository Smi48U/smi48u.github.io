# smi48u's Cybersecurity Blog & Portfolio

A minimalist, terminal-inspired personal site to document my cybersecurity learning path and share practical insights from my journey.



## 🔎 About this Project

This site was created as a personal learning challenge. I wanted to build something that looks like it belongs to someone passionate about cybersecurity — clean, minimal, a bit hackerish.

I designed the structure, wrote the content, and used ChatGPT to assist with:
- writing responsive HTML/CSS
- improving UX for mobile
- creating Markdown-powered blog rendering
- building a clean, modern card layout
- fixing tricky bugs and edge cases

**This project is 100% mine.** Every line of code, prompt, decision and revision — even if some ideas came from AI, I made sure I understood and controlled the result.

---

## 🚀 Features

- Responsive HTML/CSS layout
- Custom blog system powered by Markdown
- Syntax highlighting & command line aesthetics
- SEO-friendly and fast
- GitHub Pages ready

---

## 💡 How I Use It

- Share my learning notes, OSINT labs, threat research, and insights
- Document my journey from beginner to cybersecurity pro
- Showcase my growth to future employers

---

## 📁 Folder Structure

```
.
├── blog.html
├── blog/
│   ├── here you can add new blog posts in markdown 
│   
├── css/
│   └── styles.css
├── js/
│   ├── blog.js -> edit after placed new blog post
│   └── post.js 
└── img/
    └── fevicon.png
```

---

## 🧮 Terminalowy program HRP (Hierarchical Risk Parity)

Repo zawiera prosty skrypt terminalowy `hrp_cli.py`, który pobiera listę tickerów z pliku tekstowego, ściąga dane z Yahoo Finance i drukuje wagi HRP.

### Uruchomienie

1. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
2. Przygotuj plik z tickerami (po jednym na linię). Przykład: `tickers_example.txt`.
3. Uruchom skrypt:
   ```bash
   python hrp_cli.py --tickers-file tickers_example.txt --start 2018-01-01
   ```

Opcje dodatkowe:
- `--end YYYY-MM-DD` – opcjonalna data końcowa (domyślnie do dziś),
- `--method {ward,single,average,complete}` – metoda klasteryzacji do HRP (domyślnie `ward`).

---

## 📖 Live Site

[https://smi48u.github.io](https://smi48u.github.io)

---

## ✅ Feel free to fork, clone, or adapt

If you're building your own portfolio and want to start somewhere simple but structured — this is a good base.
