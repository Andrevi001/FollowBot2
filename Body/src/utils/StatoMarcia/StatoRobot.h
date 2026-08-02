/**
 * Enum che definisce gli  stati possibili di FollowBot2:
 *  -IDLE: stato di attesa, robot fermo.
 *  -TORRE: stato centro di fuoco, il movimento del robot e limitato a una rotazione in senso orario/antiorario per tenere il bersaglio in frame.
 *  -MOVIMENTO: stato di avvicinamento/allontanamento dal bersaglio, il robot centra il bersaglio nel frame per poi avvicinarsi/allontanarsi in base alla distanza   
 */
enum StatoRobot {
    IDLE,
    TORRE,
    MOVIMENTO
};