from include import create_app

app = create_app()

@app.template_filter('b64encode')
def base64_encode(data):
    return base64.b64encode(data).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)