# FollowBot2

**FollowBot2** è la seconda versione di [FollowBot](https://github.com/Andrevi001/FollowBot). E' un rover 2WD in grado di seguire una specifica persona ed eseguire comandi semplici tramite gesture. 

Le immagini vengono acquisite da una fotocamera collegata a una **Raspberry Pi 5** ed elaborate in locale tramite script **Python** che impiegano modelli **IA** ultra-leggeri dedicati. I dati di tracciamento e movimento calcolati dalla Pi 5 vengono inviati via **UART** a una scheda **ESP32**, che gestisce la cinematica e il controllo dei motori del robot.

---

## Tecnologie e componenti

- **Raspberry PI 5** per la cattura ed elaborazione immagini
- **ESP32** per la gestione dei movimenti
- **2x Servo 180°** per il meccanismo pan/tilt
- **1x TB6612FNG** per il controllo dei motori
- **2x Motori DC** ridotti per la trazione 2WD
- **1x LM2596** per l'alimentazione "corpo"
- **1x Convertitore DC-DC 5V 10A** per l'alimentazione PI 5 ed ESP32
- **4x Batterie 18650** per l'alimentazione del sistema
- **Software & Tools**: Python, C++, PlatformIO

---

## Upgrade rispetto a FollowBot

FollowBot è un rover che segue un volto muovendosi nello spazio e tenendosi a una distanza tra 120 cm e 170 cm dal bersaglio. 
L'elaborazione delle immagini è svolta da un server che riceve le immagini catturate dal rover restituendo i dati per il movimento. 

### Altri punti deboli di FollowBot:
- Comportamento imprevedibile in presenza di più volti nel frame.
- Perdita definitiva del tracciamento quando il soggetto usciva dal campo visivo.
- Movimento a scatti del telaio per centrare il target quando il servo di Pan raggiungeva il fine corsa (rotazione improvvisa di 90°).

### Miglioramenti introdotti in FollowBot2:
- **Hardware**: L'integrazione della Raspberry Pi 5 a bordo elimina la dipendenza dal server esterno e dalla rete Wi-Fi, consentendo l'elaborazione in loco. I nuovi motoriduttori garantiscono un movimento più fluido.
- **Software**: Ottimizzazione del controllo cinematico.

### Novità:
- Riconoscimento facciale
- Tracking di spalle
- Gesture control

---

## Versioni

Le funzionalità proposte vengono sviluppate su più versioni.

### Versione 1.0:

In questa release il robot segue un volto rilevato all'interno del frame. 
Come in FollowBot questa versione ha un comportamento imprevedibile quando ci sono più volti. 

Nel rover originale è stato impiegato YuNet per la rilevazione dei volti. In questa versione ho pensato di provare un modello alternativo: MediaPipe/BlazeFace. Confrontando i due modelli ho visto che su carta, dopo una taratura del voto di *confidence*, si hanno performance migliori. 

#### Confronto prestazioni modelli (YuNet vs BlazeFace)

| CPU Usage | RAM Usage |
| :---: | :---: |
| ![CPU_Percent](Eye/ModelPerformance/Graphs/face_tracking/CPU.png) | ![RAM_MB](Eye/ModelPerformance/Graphs/face_tracking/RAM.png) |

| Inference Latency | FPS |
| :---: | :---: |
| ![Inference_Latency_ms](Eye/ModelPerformance/Graphs/face_tracking/Inference.png) | ![fps](Eye/ModelPerformance/Graphs/face_tracking/fps.png) |

#### Considerazioni pratiche ed empiriche:
Nonostante le metriche favorevoli nei benchmark, i test sul campo evidenziano alcune limitazioni rispetto a YuNet:
- L'abbassamento della soglia di *confidence* ha introdotto falsi positivi (ombre o elementi dello sfondo scambiati per volti).
- A medie distanze (2-3 metri) il modello mostra un'accuratezza inferiore rispetto al rilevamento da vicino (< 1 metro).
- La costante per la stima della distanza era tarata sul bounding box di YuNet, risultando meno precisa con le proporzioni restituite da BlazeFace.

### Versione 2.0:
In questa versione il rover non segue più un volto ma una posa rilevata all'interno del frame.

La rilevazione delle pose è delegata a un modello IA specializzato. Per la scelta di questo modello ho effettuato un confronto tra 3 modelli:
MediaPipePose, YoLov8Pose e RTMPose. Come si vedrà dal confronto MediaPipe pose è la scelta più adeguata.

Questa versione integra l'utilizzo del **multithreading**. I thread sono: il main thread, il thread dedicato alla cattura immagine e il thread dedicato all'inferenza di MediaPipePose. L'integrazione del **multithreading**, come si vede dal confronto, porta a un leggero miglioramento (5% circa) rispetto alla versione non threaded, a costo di un utilizzo maggiore della CPU. 

#### Confronto prestazioni modelli (MediaPipePose vs YoLov8Pose vs RTMPose)

| CPU Usage | RAM Usage |
| :---: | :---: |
| ![CPU_Percent](Eye/ModelPerformance/Graphs/pose_tracking/CPU.png) | ![RAM_MB](Eye/ModelPerformance/Graphs/pose_tracking/RAM.png) |

| Inference Latency | FPS |
| :---: | :---: |
| ![Inference_Latency_ms](Eye/ModelPerformance/Graphs/pose_tracking/Inference.png) | ![fps](Eye/ModelPerformance/Graphs/pose_tracking/fps.png) |

#### Confronto prestazioni threaded e non threaded

| CPU Usage | RAM Usage |
| :---: | :---: |
| ![CPU_Percent](Eye/ModelPerformance/Graphs/thread_vs_non_thread/CPU.png) | ![RAM_MB](Eye/ModelPerformance/Graphs/thread_vs_non_thread/RAM.png) |

| FPS |
| :---: |
| ![fps](Eye/ModelPerformance/Graphs/thread_vs_non_thread/fps.png) |

#### Considerazioni pratiche ed empiriche:
Nonostante il miglioramento ridotto dato dall'integrazione del **multithreading**, riutilizzare l'ultima posa disponibile più volte porta a un movimento più fluido del meccanismo **Pan/Tilt**.

La stima della distanza si basa su misure fatte su più persone alla stessa distanza di **100 cm**. La misura utilizzata è la distanza tra le spalle. L'utilizzo di questa distanza porta a problemi di stima dovuti alla rotazione del bersaglio. Inoltre questa misura non è utilizzabile di profilo. Per evitare questi problemi il rover scarta tutte le misure che stanno sotto una soglia stabilità.


---

## Uso
1. Accendere il robot.
2. Il robot inizierà a rilevare il corpo e a muoversi in modo autonomo cercando di mantenere una distanza tra **100 cm e 160 cm** dal bersaglio.

---

## REPO
- `/Body`: Codice C++ / PlatformIO per il controllo dei motori (ESP32).
- `/Eye`: Codice Python per la computer vision e la gestione della camera (Raspberry Pi 5).
- `/Eye/Distance`: misurazioni a **100 cm** utilizzate per stimare la distanza dal bersaglio.
- `/Eye/ModelPerformance`: Benchmark e grafici sulle prestazioni dei modelli.
- `/Eye/Models`: Modelli IA utilizzati per l'inferenza.

---

## Licenza
Distribuito sotto licenza **MIT**. Vedi il file [`LICENSE`](LICENSE) per i dettagli.