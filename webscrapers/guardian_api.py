import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import torch
from threading import Thread


MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

class GuardianSentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guardian Sentiment Analyser (RoBERTa)")
        self.setup_ui()
        self.setup_menu()
    
    def setup_ui(self):
        # Input Frame
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="Search Query:").pack(side=tk.LEFT)
        self.entry = ttk.Entry(input_frame, width=40)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda event: self.start_analysis())
        
        self.analyze_btn = ttk.Button(input_frame, text="Analyse", command=self.start_analysis)
        self.analyze_btn.pack(side=tk.LEFT)
        
        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, mode='indeterminate')
        
        # Results Frame
        results_frame = ttk.Frame(self.root, padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, height=20, font=('Arial', 10))
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Stats Frame
        stats_frame = ttk.Frame(self.root, padding="10")
        stats_frame.pack(fill=tk.X)
        self.stats_label = ttk.Label(stats_frame, text="Ready")
        self.stats_label.pack()
    
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)
    
    def start_analysis(self):
        query = self.entry.get().strip()
        if not query:
            self.show_error("Please enter a search query")
            return
        
        self.analyze_btn.config(state=tk.DISABLED)
        self.progress.pack(fill=tk.X)
        self.progress.start()
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Searching Guardian for: '{query}'...\n")
        self.root.update()
        
        Thread(target=self.run_analysis, args=(query,), daemon=True).start()
    
    def run_analysis(self, query):
        try:
            # Step 1: Fetch articles from The Guardian
            api_key = "b76417ac-c6eb-425b-b47a-3eab07f74e21"  
            url = f"https://content.guardianapis.com/search?q={query}&api-key={api_key}&page-size=5&show-fields=trailText"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = data.get("response", {}).get("results", [])
            if not articles:
                self.show_result("No articles found. Try a different query.")
                return
            
            # Step 2: Analyse sentiment for each article
            self.update_results(f"\nFound {len(articles)} articles. Analysing sentiment...\n{'='*50}\n")
            
            sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
            
            for idx, article in enumerate(articles, 1):
                title = article.get("webTitle", "No title")
                snippet = article.get("fields", {}).get("trailText", title)
                
                # Truncate to model's max length (512 tokens)
                inputs = tokenizer(snippet, return_tensors="pt", truncation=True, max_length=512)
                with torch.no_grad():
                    outputs = model(**inputs)
                
                # Convert logits to probabilities
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
                pred_class = torch.argmax(probs).item()
                confidence = probs[0][pred_class].item()
                
                # Map class to label
                labels = ["negative", "neutral", "positive"]
                sentiment = labels[pred_class]
                sentiment_counts[sentiment] += 1
                
                # Format results
                self.update_results(
                    f"ARTICLE {idx}: {title}\n"
                    f"Sentiment: {sentiment.upper()} ({confidence:.1%})\n"
                    f"Excerpt: {snippet[:200]}...\n"
                    f"{'-'*50}\n"
                )
            
            # Step 3: Display summary
            total = len(articles)
            self.update_results(
                f"\nSUMMARY:\n"
                f"Positive: {sentiment_counts['positive']}/{total} ({sentiment_counts['positive']/total:.1%})\n"
                f"Neutral: {sentiment_counts['neutral']}/{total} ({sentiment_counts['neutral']/total:.1%})\n"
                f"Negative: {sentiment_counts['negative']}/{total} ({sentiment_counts['negative']/total:.1%})\n"
            )
            
            self.stats_label.config(text=f"Analysis complete for '{query}'")
            
        except requests.RequestException as e:
            self.show_error(f"API Error: {str(e)}")
        except Exception as e:
            self.show_error(f"Unexpected error: {str(e)}")
        finally:
            self.progress.stop()
            self.progress.pack_forget()
            self.analyze_btn.config(state=tk.NORMAL)
    
    def update_results(self, text):
        self.results_text.insert(tk.END, text)
        self.results_text.see(tk.END)
        self.root.update()
    
    def show_error(self, message):
        self.results_text.insert(tk.END, f"\nERROR: {message}\n")
        self.progress.stop()
        self.progress.pack_forget()
        self.analyze_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = GuardianSentimentApp(root)
    root.mainloop()