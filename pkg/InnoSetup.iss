
; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Beam DICOM"
#define MyAppVersion "1.0"
#define MyAppPublisher "Beam DICOM by Medly Tech."
#define MyAppURL "http://www.MedlyTech.com"
#define MyAppExeName "beamdicom.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{08294AAA-D48D-4B1C-A89A-8AB93D04BD4D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=dicom_converter_installer
Compression=lzma
SolidCompression=yes
OutputDir=c:\work\sw\setup
SetupIconFile=logo.ico
;WizardImageFile=logo.bmp
WizardSmallImageFile=logo_small.bmp

[INI]

Filename: {app}\settings\setupSettings.ini; Section: storage; Key: folder; String: {code:GetDicomStoragePath}


[code]
var
//Define global variables
  InfoPage: TWizardPage;
  ComboBox: TNewComboBox;
  strComboValue: String;
  ComboLabel : TNewStaticText;
  ComboBox2: TNewComboBox;
   strCombo2Value: String;
   DirePage: TInputDirWizardPage   ;
   

//Store the ComboBox string value

procedure InitializeWizard();
begin

  //InfoPage := CreateCustomPage(wpWelcome,'Settings','');


    
   DirePage := CreateInputDirPage( wpWelcome, '' , '' , '', False , '');
   
   DirePage.add('Select Dicom Folder Storage');
   

  
  
end;
function checkSelection(Sender: TWizardPage): Boolean;
begin
    result := False
end;
function GetStrComboValue(Param: String): string;
begin
result := strComboValue;
end;
function GetStrCombo2Value(Param: String): string;
begin
result := strCombo2Value;
end;
function GetDicomStoragePath(Param: String): string;
begin
result := DirePage.Values[0];
StringChangeEx(result , '\' , '\\',True);
end;


[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: dontinheritcheck

[Files]
Source: "c:\work\code\beamdicom\dist\beamdicom\beamdicom.exe"; DestDir: "{app}"; Flags: ignoreversion ;
Source: "c:\work\code\beamdicom\dist\beamdicom\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs ;
Source: "c:\work\code\beamdicom\logo.bmp"; DestDir: "{app}"; Flags:ignoreversion recursesubdirs createallsubdirs ;
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}" ; IconFilename: {app}\logo.ico
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon ;   IconFilename: {app}\logo.ico
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}" ; IconFilename: {app}\logo.ico
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: {app}\logo.ico



[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\settings\setupSettings.ini"