; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "DICOM Converter"
#define MyAppVersion "1.0"
#define MyAppPublisher "Bacon Healthcare."
#define MyAppURL "http://www.baconhealthcare.com"
#define MyAppExeName "main.exe"

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
Filename: {app}\settings\setupSettings.ini; Section: conversion; Key: format; String: {code:GetStrComboValue}
Filename: {app}\settings\setupSettings.ini; Section: storage; Key: foldername_mode; String: {code:GetStrCombo2Value}
Filename: {app}\settings\setupSettings.ini; Section: storage; Key: folder; String: {code:GetDicomStoragePath}
Filename: {app}\settings\setupSettings.ini; Section: storage; Key: tmp; String: {code:GetDicomTempStoragePath}
Filename: {app}\settings\setupSettings.ini; Section: conversion; Key: folder; String: {code:GetConversionStoragePath}
Filename: {app}\settings\setupSettings.ini; Section: client; Key: name; String: DICOM Converter
Filename: {app}\settings\setupSettings.ini; Section: facility; Key: name; String: {code:GetFacilityName}

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
   facility_name: TEdit; 

//Store the ComboBox string value
procedure ComboChange(Sender: TObject);
begin
  case ComboBox.ItemIndex of
    0:
    begin
      strComboValue := 'png';
    end;
    1:
    begin
      strComboValue := 'jpg';
    end;
     2:
    begin
      strComboValue := 'bmp';
    end;
     3:
    begin
      strComboValue := 'pdf';
    end;
  end;
end;
 //Store the ComboBox string value
procedure Combo2Change(Sender: TObject);
begin
  case ComboBox2.ItemIndex of
    0:
    begin
      strCombo2Value := 'PatientName';
    end;
    1:
    begin
      strCombo2Value := 'PatientID';
    end;
     2:
    begin
      strCombo2Value := 'Study Instance UID';
    end;
  end;
end;
procedure dicomFldComboChange(Sender: TObject);
begin
  case ComboBox2.ItemIndex of
    0:
    begin
      strCombo2Value := 'Patient Name';
    end;
    1:
    begin
      strCombo2Value := 'Patient Id';
    end;
     2:
    begin
      strCombo2Value := 'Study Instance UID';
    end;
  end;
end;
procedure InitializeWizard();
begin

  InfoPage := CreateCustomPage(wpWelcome,'Settings','');

  ComboLabel := TNewStaticText.Create(WizardForm);
  ComboLabel.Caption := 'Please Enter Facility Name:';
  ComboLabel.Top := 0;
  ComboLabel.Parent := InfoPage.Surface;

  facility_name :=   TEdit.Create(InfoPage);
  facility_name.Parent := InfoPage.Surface;
  facility_name.Top := ComboLabel.Top + ComboLabel.Height + 6; 
  facility_name.Width := 200 ;
  facility_name.Left := 0  ;
  
  


  ComboLabel := TNewStaticText.Create(WizardForm);
  ComboLabel.Caption := 'Please Select Conversion Format:';
  ComboLabel.Top := facility_name.Top + facility_name.Height + 6; 
  ComboLabel.Parent := InfoPage.Surface;

  ComboBox := TNewComboBox.Create(InfoPage);
  ComboBox.Parent := InfoPage.Surface;
  ComboBox.Top := ComboLabel.Top +ComboLabel.Height + 6;
  ComboBox.Left := 0;
  ComboBox.Width := 200;
  
  ComboBox.Style := csDropDown;
  ComboBox.Items.Add('png');
  ComboBox.Items.Add('jpg');
  ComboBox.Items.Add('bmp');
  ComboBox.Items.Add('pdf');
  ComboBox.OnChange := @ComboChange;
  
  ComboLabel := TNewStaticText.Create(WizardForm);
  ComboLabel.Caption := 'Please Select Images Folder Naming Policy:';
  ComboLabel.Top := ComboBox.Top + 26;
  ComboLabel.Parent := InfoPage.Surface;

  ComboBox2 := TNewComboBox.Create(InfoPage);
  ComboBox2.Parent := InfoPage.Surface;
  ComboBox2.Top := ComboLabel.Top + ComboLabel.Height + 6; 
  ComboBox2.Width := 200
  ComboBox2.Left := 0
  ComboBox2.Style := csDropDown;
  ComboBox2.Items.Add('Patient Name');
  ComboBox2.Items.Add('Patient Id');
  ComboBox2.Items.Add('Study Instance UID');
  ComboBox2.OnChange := @Combo2Change;

  
  
   DirePage := CreateInputDirPage( wpWelcome, '' , '' , '', False , '');
   
   DirePage.add('Select Dicom Folder Storage');
   DirePage.add('Select Conversion Folder Storage');
   DirePage.add('Select Conversion Temp. Folder Storage');

  
  
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
function GetDicomTempStoragePath(Param: String): string;
begin
result := DirePage.Values[2];
StringChangeEx(result , '\' , '\\',True);
end;
function GetConversionStoragePath(Param: String): string;
begin
result := DirePage.Values[1];
StringChangeEx(result , '\' , '\\',True);
end;
function GetFacilityName(Param: String): string;
begin
result := trim(facility_name.Text);
end;
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: dontinheritcheck

[Files]
Source: "c:\work\code\dicom_router\dist\main\main.exe"; DestDir: "{app}"; Flags: ignoreversion ;
Source: "c:\work\code\dicom_router\dist\main\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs ;
Source: "c:\work\code\dicom_router\logo.bmp"; DestDir: "{app}"; Flags:ignoreversion recursesubdirs createallsubdirs ;
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