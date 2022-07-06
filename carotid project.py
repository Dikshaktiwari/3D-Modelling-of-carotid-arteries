def show3dImage():
  
  global DISPLAY

  rho, sigma = RADIUS, SPREAD
  
 
  xl=[]
  yl=[]
  zl=[]
  xs=[]
  ys=[]
  zs=[]
  count= 0
  carotid_pts=[]
  print("Generating 3D model of Artery...")
  out = display(progress(0, 300), display_id=True)
  for i in range(0,300):
    out.update(progress(i, 300))

    name = path+"US0004_{:04d}.png".format(i)  
    
    if os.path.exists(name):
      try:
        
        img = readImage(name)
       
        cimg, loc, maxs = findMaxCorrelation(img, rho, sigma)  #calling the function for getting the points with max correlation in the image
        BPts= getBoundary(img,loc)   #calling the function to identify the bundary of artery using the opints obtain fr0om max correlation
        carotid_pts = np.array(getCarotidPts(img)) #function used for gettig the cordinate of bloackage of cordinate inside artery wall
        x_mean = np.mean(carotid_pts[:,0])
        x_std = np.std(carotid_pts[:,0])
       
        y_mean = np.mean(carotid_pts[:,1])
        y_std = np.std(carotid_pts[:,1])
 
        threshold = 0.1
        for i in carotid_pts:
          zx =(i[0]-x_mean)/x_std
          zy =(i[1]-y_mean)/y_std
          
     
          if zx < threshold and zy < threshold:
            xs.append(i[0])
            ys.append(i[1])
            zs.append(count)
       
        x=[]
        y=[]
        z=[]
        for t in range(360):
            th = t * 2 * np.pi / 360
            xp = int(loc[0] + (BPts[t] + RMIN) * np.cos(th) + 0.5)
            yp = int(loc[1] + (BPts[t] + RMIN) * np.sin(th) + 0.5)
            x.append(xp)
            y.append(yp)
            z.append(count)

        xl.append(x)
        yl.append(y)
        zl.append(z)

        count+=5

      except Exception as e:
        pass
  fig = go.Figure(data=[go.Surface(z=zl, x=xl, y=yl,colorscale="Reds_r"),go.Scatter3d(x=xs,y=ys,z=zs,mode='markers',marker=dict(size=7,color=zs,colorscale='reds',opacity=0.8))])#,surfacecolor=colours)#,layout={'colorscale':{'sequential':colours}})
  
  fig.update_layout(title='Artries visualization', autosize=True,)
  
  now = datetime.now()
  dt_string = now.strftime("%d_%m_%Y_%H_%M")
  fig.write_html(f"/content/sample_data/Ultrasound_{dt_string}.html")
  files.download(f"/content/sample_data/Ultrasound_{dt_string}.html")
  print("Model generated and downloaded successfully !!")
  

def main():
  
  show3dImage()
  
if _name_=="main":
	main()
