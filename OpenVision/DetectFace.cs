﻿using Emgu.CV;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;

namespace OpenVision
{
    public static class DetectFace
    {
        public static void Detect(
           IInputArray image, String faceFileName,// String eyeFileName,
           List<Rectangle> faces,// List<Rectangle> eyes,
           out long detectionTime)
        {
            Stopwatch watch;

            using (InputArray iaImage = image.GetInputArray())
            {

                using (CascadeClassifier face = new CascadeClassifier(faceFileName))
                //using (CascadeClassifier eye = new CascadeClassifier(eyeFileName))
                {
                    watch = Stopwatch.StartNew();

                    using (UMat ugray = new UMat())
                    {
                        CvInvoke.CvtColor(image, ugray, Emgu.CV.CvEnum.ColorConversion.Bgr2Gray);

                        //normalizes brightness and increases contrast of the image
                        CvInvoke.EqualizeHist(ugray, ugray);

                        //Detect the faces  from the gray scale image and store the locations as rectangle
                        //The first dimensional is the channel
                        //The second dimension is the index of the rectangle in the specific channel                     
                        Rectangle[] facesDetected = face.DetectMultiScale(
                           ugray,
                           1.1,
                           10,
                           new Size(20, 20));

                        faces.AddRange(facesDetected);

                        /*foreach (Rectangle f in facesDetected)
                        {
                            //Get the region of interest on the faces
                            using (UMat faceRegion = new UMat(ugray, f))
                            {
                                Rectangle[] eyesDetected = eye.DetectMultiScale(
                                   faceRegion,
                                   1.1,
                                   10,
                                   new Size(20, 20));

                                foreach (Rectangle e in eyesDetected)
                                {
                                    Rectangle eyeRect = e;
                                    eyeRect.Offset(f.X, f.Y);
                                    eyes.Add(eyeRect);
                                }
                            }
                    }*/
                    }
                    watch.Stop();
                }
            }
            detectionTime = watch.ElapsedMilliseconds;
        }
    }
}
