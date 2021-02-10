tarifa_old = [
	(0,100,0.09),
	(100,150,0.3),
	(150,200,0.4),
	(200,250,0.6),
	(250,300,0.8),
	(300,350,1.5),
	(350,500,1.8),
	(500,1000,2.0),
	(1000,5000,3.0),
	(5000,5.0)
		]

TARIFA = [
	(0,100,0.33),
	(100,150,1.07),
	(150,200,1.43),
	(200,250,2.46),
	(250,300,3.00),
	(300,350,4.00),
	(350,400,5.00),
	(400, 450,6.00),
	(450,500,7.00),
	(500,600,9.20),
	(600,700,9.45),
	(700,1000,9.85),
	(1000,1800,10.80),
	(1800,2600,11.80),
	(2600,3400,12.90),
	(3400,4200,13.95),
	(4200,5000,15.00),
	(5000,20.0)    
	]
def calcularImporte(consumo, tarifa = TARIFA):
	importe = 0.0
	for r in tarifa:		
		if consumo <= 0:
			break
			
		elif r is max(tarifa):
			importe = importe + (consumo * r[1])
			consumo = 0
					
		elif consumo >= (r[1]-r[0]):
			importe = importe + ((r[1]-r[0]) * r[2])
			consumo = 0 if (consumo - (r[1]-r[0])) < 0 else consumo - (r[1]-r[0])
			
		else:
			importe = importe + (consumo * r[2])				
			consumo = 0	
				
	return f"{importe:.2f}"
		
		
