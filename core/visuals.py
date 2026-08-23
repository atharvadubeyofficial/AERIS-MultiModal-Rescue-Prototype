import cv2
import numpy as np

def draw_detections(frame, targets):
    for t in targets:
        x1,y1,x2,y2=t["bbox"]
        label=f"T{t['target_id']} {t['priority']} {t['score']:.0f}%"
        thickness=4 if t["priority"]=="CRITICAL" else 3 if t["priority"]=="HIGH" else 2
        cv2.rectangle(frame,(x1,y1),(x2,y2),(255,180,0),thickness)
        cv2.rectangle(frame,(x1,max(0,y1-28)),(min(frame.shape[1],x1+180),y1),(30,30,30),-1)
        cv2.putText(frame,label,(x1+5,max(18,y1-8)),cv2.FONT_HERSHEY_SIMPLEX,0.55,(255,255,255),2)
    return frame

def mission_map_image(width,height,targets):
    canvas=np.zeros((360,700,3),dtype=np.uint8); canvas[:]=(24,29,36)
    cv2.putText(canvas,"AERIS MISSION MAP",(20,35),cv2.FONT_HERSHEY_SIMPLEX,0.9,(240,240,240),2)
    drone=(90,290); cv2.circle(canvas,drone,12,(255,190,0),-1)
    cv2.putText(canvas,"UAV",(65,325),cv2.FONT_HERSHEY_SIMPLEX,0.55,(240,240,240),1)
    points=[(260,100),(410,180),(560,90),(520,280),(320,280)]
    for i,t in enumerate(targets[:5]):
        p=points[i]; cv2.circle(canvas,p,15 if t["priority"]=="CRITICAL" else 11,(30,70,220),-1)
        cv2.putText(canvas,f"T{t['target_id']} {t['priority']}",(p[0]-25,p[1]-22),
                    cv2.FONT_HERSHEY_SIMPLEX,0.45,(245,245,245),1)
    if targets:
        cv2.line(canvas,drone,points[0],(80,210,255),3)
    cv2.putText(canvas,"Illustrative mission route",(20,350),cv2.FONT_HERSHEY_SIMPLEX,0.45,(170,180,190),1)
    return cv2.cvtColor(canvas,cv2.COLOR_BGR2RGB)
