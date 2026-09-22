import pandas as pd
import matplotlib.pyplot as plt

MediaPipePose = pd.read_csv('../../Pose_tracking_stats/MediaPipePose.csv')
YoLov8Pose = pd.read_csv('../../Pose_tracking_stats/YoLo.csv')
RTMPose = pd.read_csv('../../Pose_tracking_stats/RTMPose.csv')


MPose_pr = []
YoLo_pr = []
RTMP_pr = []

MPose_pr.append(MediaPipePose["CPU_Percent"].mean())
MPose_pr.append(MediaPipePose["RAM_MB"].mean())
MPose_pr.append(MediaPipePose["Inference_Latency_ms"].mean())
mean_tot_latency = MediaPipePose["Total_Latency_ms"].mean()
#calcolo fps
MPose_pr.append(1000/mean_tot_latency)

YoLo_pr.append(YoLov8Pose["CPU_Percent"].mean())
YoLo_pr.append(YoLov8Pose["RAM_MB"].mean())
YoLo_pr.append(YoLov8Pose["Inference_Latency_ms"].mean())
mean_tot_latency = YoLov8Pose["Total_Latency_ms"].mean()
#calcolo fps
YoLo_pr.append(1000/mean_tot_latency)

RTMP_pr.append(RTMPose["CPU_Percent"].mean())
RTMP_pr.append(RTMPose["RAM_MB"].mean())
RTMP_pr.append(RTMPose["Inference_Latency_ms"].mean())
mean_tot_latency = RTMPose["Total_Latency_ms"].mean()
#calcolo fps
RTMP_pr.append(1000/mean_tot_latency)

categorie = ['CPU_Percent(%)', 'RAM_MB', 'Inference_Latency_ms', 'fps']



def grafico(categoria, valore1, valore2, valore3, label1, label2, label3, titolo, file):
    larghezza_barra = 0.10
    plt.figure(figsize=(10, 6))

    plt.bar(1 - larghezza_barra, valore1, larghezza_barra, label= label1, color='blue', alpha=0.7)
    plt.bar(1 , valore2, larghezza_barra, label= label2, color='orange', alpha=0.7)
    plt.bar(1 + larghezza_barra, valore3, larghezza_barra, label= label3, color='red', alpha=0.7)

    plt.title(titolo)
    plt.xticks([1], [categoria])

    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.savefig(file, dpi=300, bbox_inches='tight')
    plt.close()

grafico(categorie[0], MPose_pr[0], YoLo_pr[0], RTMP_pr[0], 'MediaPipePose', 'YoLov8Pose', 'RTMPose', "Confronto Percentuale CPU", "CPU.png")
grafico(categorie[1], MPose_pr[1], YoLo_pr[1], RTMP_pr[1], 'MediaPipePose', 'YoLov8Pose', 'RTMPose', "Confronto RAM in MB", "RAM.png")
grafico(categorie[2], MPose_pr[2], YoLo_pr[2], RTMP_pr[2], 'MediaPipePose', 'YoLov8Pose', 'RTMPose', "Confronto Inference Latency in ms", "Inference.png")
grafico(categorie[3], MPose_pr[3], YoLo_pr[3], RTMP_pr[3], 'MediaPipePose', 'YoLov8Pose', 'RTMPose', "Confronto fps", "fps.png")