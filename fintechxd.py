from flask import Flask, request, jsonify, render_template_string
import yfinance as yf

app = Flask(__name__)

HTML_SEARCH = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Ações</title>
</head>
<body>
    <h1>Pesquisar Ação</h1>
    <form action="/search" method="get">
        <label for="query">Digite o nome ou símbolo da ação:</label><br>
        <input type="text" id="query" name="query" placeholder="Ex: Apple, AAPL, PETR4" required><br><br>
        <button type="submit">Buscar</button>
    </form>
    <h2>Resultados</h2>
    <ul>
        {% for ticker in tickers %}
        <li><a href="/stock_report?ticker={{ ticker }}">{{ ticker }}</a></li>
        {% endfor %}
    </ul>
</body>
</html>
"""

def generate_stock_report(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)

        if not stock.info:
            return {"error": f"Ação com símbolo '{ticker_symbol}' não encontrada."}

        stock_info = stock.info

        report = {
            "nome": stock_info.get('shortName', 'N/A'),
            "simbolo": ticker_symbol.upper(),
            "setor": stock_info.get('sector', 'N/A'),
            "industria": stock_info.get('industry', 'N/A'),
            "pais": stock_info.get('country', 'N/A'),
            "preco_atual": stock_info.get('currentPrice', 'N/A'),
            "alta_52_semanas": stock_info.get('fiftyTwoWeekHigh', 'N/A'),
            "baixa_52_semanas": stock_info.get('fiftyTwoWeekLow', 'N/A'),
            "capitalizacao_mercado": stock_info.get('marketCap', 'N/A'),
            "volume_medio": stock_info.get('averageVolume', 'N/A'),
            "dividend_yield": stock_info.get('dividendYield', 'N/A'),
            "lucro_por_acao": stock_info.get('trailingEps', 'N/A'),
            "pl_ratio": stock_info.get('trailingPE', 'N/A'),
            "descricao": stock_info.get('longBusinessSummary', 'N/A')[:300] + "..."
        }
        return report

    except Exception as e:
        return {"error": f"Erro ao gerar o relatório: {e}"}

@app.route('/')
def home():
    return render_template_string(HTML_SEARCH, tickers=[])

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if not query:
        return render_template_string(HTML_SEARCH, tickers=[])

    try:
        stock = yf.Ticker(query)
        if stock.info:
            tickers = [query]
        else:
            tickers = []
    except:
        tickers = []

    return render_template_string(HTML_SEARCH, tickers=tickers)

@app.route('/stock_report', methods=['GET'])
def stock_report():
    ticker = request.args.get('ticker', '').strip()
    if not ticker:
        return jsonify({"error": "Por favor, forneça um símbolo de ação válido."}), 400

    report = generate_stock_report(ticker)
    return jsonify(report)

if __name__ == "__main__":
    app.run(debug=True)