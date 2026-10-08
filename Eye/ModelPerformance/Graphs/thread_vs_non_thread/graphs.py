import pandas as pd
import matplotlib.pyplot as plt

non_threaded = pd.read_csv('../../Pose_tracking_stats/MediaPipePose.csv')
threaded = pd.read_csv('../../Pose_tracking_stats/MediaPipeThreaded.csv')

non_threaded_pr = []
threaded_pr = []

non_threaded_pr.append(non_threaded["CPU_Percent"].mean())
non_threaded_pr.append(non_threaded["RAM_MB"].mean())
non_threaded_pr.append(non_threaded["Inference_Latency_ms"].mean())
mean_tot_latency = non_threaded["Total_Latency_ms"].mean()
#calcolo fps
non_threaded_pr.append(1000/mean_tot_latency)

threaded_pr.append(threaded["CPU_Percent"].mean())
threaded_pr.append(threaded["RAM_MB"].mean())
threaded_pr.append(threaded["Inference_Latency_ms"].mean())
mean_tot_latency = threaded["Total_Latency_ms"].mean()
#calcolo fps
threaded_pr.append(1000/mean_tot_latency)

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
    plt.close()

grafico(categorie[0], non_threaded_pr[0], threaded_pr[0], 'non_threaded', 'threaded', "Confronto Percentuale CPU", "CPU.png")
grafico(categorie[1], non_threaded_pr[1], threaded_pr[1], 'non_threaded', 'threaded', "Confronto RAM in MB", "RAM.png")
grafico(categorie[3], non_threaded_pr[3], threaded_pr[3], 'non_threaded', 'threaded', "Confronto fps", "fps.png")