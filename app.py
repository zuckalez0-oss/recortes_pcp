from flask import Flask, render_template, request, redirect, url_for, flash
import database
import datetime


app = Flask(__name__)
app.secret_key = 'supersecretkey' # Necessário para mensagens flash

# Garante que o banco de dados seja inicializado ao iniciar o app
with app.app_context():
    database.init_db()

@app.route('/')
def index():
    """Rota para a página inicial de entrada de dados."""
    # Pre-popula a data atual para facilitar
    hoje = datetime.date.today().isoformat()
    return render_template('index.html', hoje=hoje)

@app.route('/add_recorte', methods=['POST'])
def add_recorte():
    """Adiciona um novo recorte de produção ao banco de dados."""
    if request.method == 'POST':
        codigo_peca = request.form['codigo_peca']
        quantidade = request.form['quantidade']
        medidaa = request.form['medidaa']
        medidab = request.form['medidab']
        data_producao = request.form['data_producao']
        turno = request.form['turno']
        observacoes = request.form['observacoes']

        if not codigo_peca or not quantidade or not medidaa or not medidab or not data_producao or not turno or not observacoes:
            flash('Por favor, preencha todos os campos obrigatórios!', 'error')
            return redirect(url_for('index'))

        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError
        except ValueError:
            flash('Quantidade deve ser um número inteiro positivo!', 'error')
            return redirect(url_for('index'))

        with database.connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recortes (codigo_peca, quantidade,medidaa, medidab, data_producao, turno, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (codigo_peca, quantidade, data_producao, turno, observacoes, medidaa, medidab))
            conn.commit()
        flash('Recorte adicionado com sucesso!', 'success')
        return redirect(url_for('index'))

@app.route('/view_recortes')
def view_recortes():
    """Rota para a página de visualização dos recortes para o PCP."""
    with database.connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM recortes ORDER BY data_producao DESC, id DESC')
        recortes = cursor.fetchall()
    return render_template('view_recortes.html', recortes=recortes)

@app.route('/delete_recorte/<int:recorte_id>', methods=['POST'])
def delete_recorte(recorte_id):
    """Exclui um recorte de produção."""
    with database.connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM recortes WHERE id = ?', (recorte_id,))
        conn.commit()
    flash('Recorte excluído com sucesso!', 'success')
    return redirect(url_for('view_recortes'))



if __name__ == '__main__':
    # Define o host como '0.0.0.0' para ser acessível de outros dispositivos na rede
    # e a porta como 5000 (padrão do Flask).
    # debug=True é ótimo para desenvolvimento, mas remova em produção.
    app.run(host='0.0.0.0', port=5000, debug=True)
