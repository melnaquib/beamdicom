#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>

int main(int argc, char *argv[])
{
//  QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
  QString folderName = "/usr/share/backgrounds/gnome/";

  QGuiApplication app(argc, argv);

  QQmlApplicationEngine engine;

  engine.rootContext()->setContextProperty("imagesFolder", folderName);

//  engine.rootContext().setContextProperty("imagesFolder", foldername)
  engine.rootContext()->setContextProperty("patientID", "patient_id");
//  patient_name = str(patient_name).replace('^', ' ');
  engine.rootContext()->setContextProperty("patientName", "FName LName");
  QStringList files;
  files
      << "adwaita-day.jpg" << "Blinds.jpg" << "Flowerbed.jpg"
      << "Stones.jpg" << "adwaita-lock.jpg" << "Bokeh_Tails.jpg"
      << "FootFall.png" << "Terraform-green.jpg"
         ;
  engine.rootContext()->setContextProperty("files", files);
//  engine.load(QUrl("./studyImageViewer/main.qml"));


//  engine.load(QUrl(QLatin1String("qrc:/main.qml")));
  engine.load(QUrl(QLatin1String("../studyImageViewer/main.qml")));

  return app.exec();
}
