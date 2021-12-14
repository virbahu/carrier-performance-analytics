import numpy as np
def analyze_carrier(carrier_data, periods=12):
    metrics={}
    for metric in ["on_time_pct","damage_rate","cost_per_shipment","claims_pct","transit_time_days"]:
        values=carrier_data.get(metric,[])
        if not values: continue
        v=np.array(values[-periods:])
        trend=np.polyfit(range(len(v)),v,1)[0]
        metrics[metric]={"current":round(v[-1],2),"avg":round(np.mean(v),2),"trend":round(trend,3),
                        "direction":"improving" if (trend<0 and metric in ("damage_rate","cost_per_shipment","claims_pct","transit_time_days")) or (trend>0 and metric=="on_time_pct") else "declining"}
    targets={"on_time_pct":95,"damage_rate":0.5,"cost_per_shipment":150,"claims_pct":1.0,"transit_time_days":3.0}
    scorecard={}
    for m,data in metrics.items():
        target=targets.get(m,0)
        if m in ("damage_rate","cost_per_shipment","claims_pct","transit_time_days"):
            scorecard[m]=round(min(100,max(0,(target/max(data["current"],0.01))*100)),1)
        else:
            scorecard[m]=round(min(100,max(0,(data["current"]/target)*100)),1)
    overall=round(np.mean(list(scorecard.values())),1) if scorecard else 0
    return {"metrics":metrics,"scorecard":scorecard,"overall_score":overall,
            "grade":"A" if overall>=90 else "B" if overall>=75 else "C" if overall>=60 else "F"}
if __name__=="__main__":
    data={"on_time_pct":[93,94,92,95,94,96,95,97,96,95,96,97],
          "damage_rate":[0.8,0.7,0.9,0.6,0.5,0.6,0.4,0.5,0.3,0.4,0.3,0.3],
          "cost_per_shipment":[160,158,155,152,150,148,145,143,140,138,135,132]}
    r=analyze_carrier(data)
    print(f"Grade: {r['grade']} ({r['overall_score']})")
