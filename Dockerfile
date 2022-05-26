FROM fusuf/asenauserbot:latest
RUN git clone https://github.com/xtq067/kartof /root/kartof
WORKDIR /root/kartof/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]
