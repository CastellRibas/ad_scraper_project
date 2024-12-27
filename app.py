from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
from flask import Flask, render_template, jsonify
import os

# Configura la app Flask
app = Flask(__name__)

# Configuración del cliente Google Ads API
credentials_path = os.path.join(os.getcwd(), "credentials.json")  # Asegúrate de tener este archivo en tu proyecto
client = GoogleAdsClient.load_from_storage(credentials_path)

# Función para obtener datos de campañas
def get_ads_data(customer_id):
    try:
        query = """
        SELECT
            campaign.id,
            campaign.name,
            metrics.clicks,
            metrics.impressions,
            metrics.ctr
        FROM campaign
        WHERE segments.date DURING LAST_30_DAYS
        """
        response = client.service.google_ads.search(customer_id=customer_id, query=query)
        data = []
        for row in response:
            data.append({
                "id": row.campaign.id,
                "name": row.campaign.name,
                "clicks": row.metrics.clicks,
                "impressions": row.metrics.impressions,
                "ctr": row.metrics.ctr,
            })
        return data
    except GoogleAdsException as ex:
        print(f"Error: {ex}")
        return []

# Ruta principal para mostrar el dashboard
@app.route("/")
def home():
    customer_id = "INSERT_CUSTOMER_ID_HERE"  # Cambia esto por un ID real
    campaigns = get_ads_data(customer_id)
    return render_template("dashboard.html", campaigns=campaigns)

# Ejecutar la app solo si este es el archivo principal
if __name__ == "__main__":
    app.run(debug=True, port=8000)  # Cambié el puerto a 8000
