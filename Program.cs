using AForge;
using AForge.Imaging;
using AForge.Imaging.Filters;
using AForge.Math.Geometry;
using Emgu.CV;
using Emgu.CV.UI;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Runtime.InteropServices;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace OpenVision
{
    class Program
    {
        [DllImport("kernel32.dll")]
        static extern IntPtr GetConsoleWindow();

        [DllImport("user32.dll")]
        static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        const int SW_HIDE = 0;
        const int SW_SHOW = 5;

        static Blob square;

        static void Main(string[] args)
        {
            var handle = GetConsoleWindow();

            ShowWindow(handle, SW_HIDE);

            var capture = new Capture();

            var viewer = new ImageViewer();

            Application.Idle += (sdr, evt) =>
            {
                var frame = capture.QueryFrame();

                ProcessImage(frame.Bitmap);

                viewer.Image = frame;
            };

            var btn = new Button();

            btn.Click += async (sender, e) =>
            {
                await Task.Factory.StartNew(() =>
                {
                    var crops = crop(viewer.Image.Bitmap);

                    var result = SendFileToServer(crops);

                    MessageBox.Show(result, "OpenVision", MessageBoxButtons.OK, MessageBoxIcon.Information);
                });
            };

            viewer.Controls.Add(btn);

            viewer.AcceptButton = btn;

            viewer.ShowDialog();
        }

        public static MemoryStream crop(Bitmap bitmap)
        {
            var ms = new MemoryStream();

            var cropRect = new Rectangle(square.Rectangle.X, square.Rectangle.Y, square.Rectangle.Width, square.Rectangle.Height);

            Bitmap target = new Bitmap(cropRect.Width, cropRect.Height);

            using (Graphics g = Graphics.FromImage(target))
            {
                g.DrawImage(bitmap, new Rectangle(0, 0, target.Width, target.Height), cropRect, GraphicsUnit.Pixel);
            }

            target.Save(ms, System.Drawing.Imaging.ImageFormat.Png);

            /*File.WriteAllBytes(@"C:\Users\id4ni10\Desktop\_crop.png", ms.ToArray());
            bitmap.Save(@"C:\Users\id4ni10\Desktop\crop.png");*/

            return ms;
        }

        private static Point[] ToPointsArray(List<IntPoint> points)
        {
            Point[] array = new Point[points.Count];

            for (int i = 0, n = points.Count; i < n; i++)
            {
                array[i] = new Point(points[i].X, points[i].Y);
            }

            return array;
        }

        private static string SendFileToServer(MemoryStream image)
        {
            byte[] fileContents = image.ToArray();

            var queryString = System.Web.HttpUtility.ParseQueryString(string.Empty);
            queryString["language"] = "pt";
            var uri = "https://api.projectoxford.ai/vision/v1.0/ocr?" + queryString;

            Uri webService = new Uri(uri);
            var requestMessage = new HttpRequestMessage(HttpMethod.Post, webService);
            requestMessage.Headers.ExpectContinue = false;

            var multiPartContent = new MultipartFormDataContent("Boundary");
            var byteArrayContent = new ByteArrayContent(fileContents);
            byteArrayContent.Headers.Add("Content-Type", "application/octet-stream");
            multiPartContent.Add(byteArrayContent, "content", "image");
            requestMessage.Content = multiPartContent;

            var httpClient = new HttpClient();

            httpClient.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", ""); //<-- key here
            try
            {
                var httpRequest = httpClient.SendAsync(requestMessage, HttpCompletionOption.ResponseContentRead, CancellationToken.None);

                var httpResponse = httpRequest.Result;
                var statusCode = httpResponse.StatusCode;
                var responseContent = httpResponse.Content;

                if (responseContent != null)
                {
                    var stringContentsTask = responseContent.ReadAsStringAsync();
                    var stringContents = stringContentsTask.Result;

                    return stringContents;
                }

                return "responseContent is null";
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);

                return ex.Message;
            }
        }

        private static void ProcessImage(Bitmap bitmap)
        {
            var bitmapData =
                bitmap.LockBits(new Rectangle(0, 0, bitmap.Width, bitmap.Height), ImageLockMode.ReadWrite, bitmap.PixelFormat);

            var colorFilter = new ColorFiltering();

            colorFilter.Red = new IntRange(0, 64);
            colorFilter.Green = new IntRange(0, 64);
            colorFilter.Blue = new IntRange(0, 64);
            colorFilter.FillOutsideRange = false;

            colorFilter.ApplyInPlace(bitmapData);

            var blobCounter = new BlobCounter();

            blobCounter.FilterBlobs = true;
            blobCounter.MinHeight = 5;
            blobCounter.MinWidth = 5;

            blobCounter.ProcessImage(bitmapData);
            var blobs = blobCounter.GetObjectsInformation();
            bitmap.UnlockBits(bitmapData);

            square = (from blob in blobs orderby blob.Area descending select blob).FirstOrDefault();

            var shapeChecker = new SimpleShapeChecker();

            Graphics g = Graphics.FromImage(bitmap);
            Pen redPen = new Pen(Color.Red, 2);

            try
            {
                List<IntPoint> corners;

                List<IntPoint> edgePoints = blobCounter.GetBlobsEdgePoints(square);

                if (shapeChecker.IsConvexPolygon(edgePoints, out corners))
                {
                    var subType = shapeChecker.CheckPolygonSubType(corners);

                    Pen pen = null;

                    if (subType == PolygonSubType.Rectangle && corners.Count == 4)
                    {
                        pen = redPen;

                        g.DrawPolygon(pen, ToPointsArray(corners));
                    }
                }

                redPen.Dispose();
                g.Dispose();
            }
            catch { }
        }
    }
}
