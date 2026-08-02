import pandas as pd
import matplotlib.pyplot as plt

YuNet = pd.read_csv('../YuNet_Performance.csv')
MediaPipe = pd.read_csv('../MediaPipe_Performance.csv')

YuNet_pr = []
MediaPipe_pr = []

YuNet_pr.append(YuNet["CPU_Percent"].mean())
YuNet_pr.append(YuNet["RAM_MB"].mean())
YuNet_pr.append(YuNet["Inference_Latency_ms"].mean())
mean_tot_latency = YuNet["Total_Latency_ms"].mean()
#calcolo fps
YuNet_pr.append(1000/mean_tot_latency)

MediaPipe_pr.append(MediaPipe["CPU_Percent"].mean())
MediaPipe_pr.append(MediaPipe["RAM_MB"].mean())
MediaPipe_pr.append(MediaPipe["Inference_Latency_ms"].mean())
mean_tot_latency = MediaPipe["Total_Latency_ms"].mean()
#calcolo fps
MediaPipe_pr.append(1000/mean_tot_latency)

categorie = ['CPU_Percent(%)', 'RAM_MB', 'Inference_Latency_ms', 'fps']



def grafico(categoria, valore1, valore2, label1, label2, titolo, file):
    larghezza_barra = 0.10
    plt.figure(figsize=(10, 6))

    plt.bar(1 - larghezza_barra/2, valore1, larghezza_barra, label= label1, color='blue', alpha=0.7)
    plt.bar(1 + larghezza_barra/2, valore2, larghezza_barra, label= label2, color='orange', alpha=0.7)

    plt.title(titolo)
    plt.xticks([1], [categoria])

    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.savefig(file, dpi=300, bbox_inches='tight')

grafico(categorie[0], YuNet_pr[0], MediaPipe_pr[0], 'YuNet', 'MediaPipe', "Confronto Percentuale CPU", "CPU.png")
grafico(categorie[1], YuNet_pr[1], MediaPipe_pr[1], 'YuNet', 'MediaPipe', "Confronto RAM in MB", "RAM.png")
grafico(categorie[2], YuNet_pr[2], MediaPipe_pr[2], 'YuNet', 'MediaPipe', "Confronto Inference Latency in ms", "Inference.png")
grafico(categorie[3], YuNet_pr[3], MediaPipe_pr[3], 'YuNet', 'MediaPipe', "Confronto fps", "fps.png")