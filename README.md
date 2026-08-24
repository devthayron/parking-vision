# Sistema de Detecção de Vagas em Estacionamentos com Visão Computacional

Sistema desenvolvido em Python capaz de identificar quais vagas estão livres ou ocupadas em um estacionamento.

## 🎥 Demonstração

![Demonstração do Parking Vision](assets/demo.gif)

O vídeo do estacionamento utilizado como entrada foi obtido a partir do [Kaggle](https://www.kaggle.com/datasets/iasadpanwhar/parking-lot-detection-counter).

A detecção e classificação das vagas foram desenvolvidas neste projeto utilizando técnicas de processamento de imagens com OpenCV.

Cada vaga é numerada e classificada visualmente como:

- 🟩 Verde — vaga livre
- 🟥 Vermelho — vaga ocupada

O sistema também exibe a quantidade de vagas disponíveis.

## Como funciona

As regiões das vagas são definidas previamente utilizando o **OpenCV** e armazenadas no arquivo `spaces.pkl`, que já acompanha o projeto com as coordenadas configuradas.

Durante o processamento, cada frame é tratado com técnicas de processamento de imagens e cada vaga é analisada individualmente.

A quantidade de pixels detectados em cada região é utilizada para classificar a vaga como livre ou ocupada.

> O sistema possui um modo de debug (`config.py`) que auxilia na calibração do `SPACE_THRESHOLD`. Esse valor pode exigir ajustes conforme o cenário.

## Tecnologias

- Python
- OpenCV
- NumPy

## 📁 Estrutura do projeto

```text
parking-vision/
├── assets/
│   └── demo.gif
├── media/
│   ├── demo.mp4
│   ├── parking.png
│   └── video.mp4
├── config.py
├── detector.py
├── main.py
├── setup_spaces.py
├── spaces.pkl
├── requirements.txt
├── README.md
└── LICENSE
```

## Como executar

```bash
git clone https://github.com/devthayron/parking-vision.git
cd parking-vision

python3 -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
# venv\Scripts\activate

pip install -r requirements.txt

python main.py
```

O vídeo processado é salvo em:

```text
media/video_result.mp4
```

Para utilizar outro vídeo ou estacionamento, altere o `INPUT_VIDEO` no `config.py` e execute o `setup_spaces.py` para redefinir as regiões das vagas:

```bash
python setup_spaces.py
```

> Isso permite redefinir as regiões das vagas e gerar um novo `spaces.pkl`.

Durante a execução:

- `Q` — encerra a aplicação.

## Próximos passos

- Aprimorar a detecção em tempo real.
- Tornar o sistema mais robusto a diferentes condições de iluminação e cenários.
- Explorar métodos de detecção baseados em aprendizado de máquina.

## Autor

**Thayron Higlânder**

LinkedIn: [https://www.linkedin.com/in/thayron-higlander](https://www.linkedin.com/in/thayron-higlander)

## Licença

Este projeto está sob a licença [MIT](LICENSE).