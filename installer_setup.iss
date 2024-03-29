; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "DICOM Converter"
#define MyAppVersion "1.0"
#define MyAppPublisher "Bacon Healthcare."
#define MyAppURL "http://www.baconhealthcare.com"
#define MyAppExeName "DicomConverter.exe"
#define MyDateTimeString GetDateTimeString('dd/mm/yyyy hh:nn:ss', '-', ':');
#define FileNamePattern "dicom_converter_installer" + " " + GetDateTimeString('dd-mm-yyyy hh-nn-ss', '-', ':');
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
OutputBaseFilename={#FileNamePattern}
Compression=lzma
SolidCompression=yes
OutputDir=C:\work\sw\setup
SetupIconFile=logo.ico
;WizardImageFile=logo.bmp
WizardSmallImageFile=logo_small.bmp
AlwaysRestart=yes

[INI]
;Filename: {app}\settings\setupSettings.ini; Section: conversion; Key: format; String: {code:GetStrComboValue}
Filename: {app}\settings\setupSettings.ini; Section: storage; Key: foldername_mode; String: {code:GetStrCombo2Value}
Filename: {app}\settings\setupSettings.ini; Section: storage; Key: folder; String: {code:GetDicomStoragePath}
Filename: {app}\settings\setupSettings.ini; Section: storage; Key: tmp; String: {code:GetDicomTempStoragePath}
Filename: {app}\settings\setupSettings.ini; Section: conversion; Key: folder; String: {code:GetConversionStoragePath}
Filename: {app}\settings\setupSettings.ini; Section: client; Key: name; String: DICOM Converter
Filename: {app}\settings\setupSettings.ini; Section: facility; Key: name; String: {code:GetFacilityName}
Filename: {app}\settings\setupSettings.ini; Section: facility; Key: logo; String: {code:GetFacilityLogoPath}

[code]
var
//Define global variables
  InfoPage: TInputFileWizardPage;
  ComboBox: TNewComboBox;
  strComboValue: String;
  ComboLabel : TNewStaticText;
  ComboBox2: TNewComboBox;
   strCombo2Value: String;
   DirePage: TInputDirWizardPage   ;
   facility_name: TEdit;
   PlayerSettingsPage: TInputFileWizardPage;
   AvatarIndex: Integer;

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
var
Delta: Integer;
begin

  InfoPage := CreateInputFilePage(wpSelectComponents,'Settings','','');

  ComboLabel := TNewStaticText.Create(WizardForm);
  ComboLabel.Caption := 'Please Enter Facility Name:';
  ComboLabel.Top := 0;
  ComboLabel.Parent := InfoPage.Surface;

  facility_name :=   TEdit.Create(InfoPage);
  facility_name.Parent := InfoPage.Surface;
  facility_name.Top := ComboLabel.Top + ComboLabel.Height + 6;
  facility_name.Width := 200 ;
  facility_name.Left := 0  ;

  AvatarIndex := InfoPage.Add('Facility Logo:', 'Image files|*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ico;|All files|*.*', '.jpg');
  Delta :=
    facility_name.Top + facility_name.Height + 10 - InfoPage.PromptLabels[AvatarIndex].Top;
 InfoPage.PromptLabels[AvatarIndex].Top := InfoPage.PromptLabels[AvatarIndex].Top + Delta;
 InfoPage.Edits[AvatarIndex].Top := InfoPage.Edits[AvatarIndex].Top + Delta;
  InfoPage.Buttons[AvatarIndex].Top := InfoPage.Buttons[AvatarIndex].Top + Delta;





  ComboLabel := TNewStaticText.Create(WizardForm);
  ComboLabel.Caption := 'Please Select Images Folder Naming Policy:';
  ComboLabel.Top := InfoPage.Buttons[AvatarIndex].Top + InfoPage.Buttons[AvatarIndex].Height + 26;
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
procedure CurStepChanged(CurStep: TSetupStep);
var
  AvatarSource: string;
  AvatarDest: string;
begin
  if CurStep = ssPostInstall then
  begin
    AvatarSource := InfoPage.Edits[AvatarIndex].Text;
    AvatarDest := ExpandConstant('{app}\' + ExtractFileName(AvatarSource));
    Log(Format('Installing avatar from "%s" to "%s"', [AvatarSource, AvatarDest]));
    if FileCopy(AvatarSource, AvatarDest, False) then
    begin
      Log('Avatar installer');
    end
      else
    begin
      Log('Error installing avatar');
    end;
  end;
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
function GetFacilityLogoPath(Param: String): string;
begin
result := InfoPage.Edits[AvatarIndex].Text;
result := ExpandConstant('{app}\' + ExtractFileName(result));
StringChangeEx(result , '\' , '\\',True);
end;
function MyDateTimeString(Param: String): String;
begin
  Result := GetDateTimeString('yyyy.mm.dd_hh.nn.ss', #0, #0);
end;
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: dontinheritcheck

[Files]
Source: "C:\work\code\dicom_router\dist\DicomConverter\DicomConverter.exe"; DestDir: "{app}"; Flags: ignoreversion ;
Source: "C:\work\code\dicom_router\dist\DicomConverter\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs ;
Source: "C:\work\code\dicom_router\logo.bmp"; DestDir: "{app}"; Flags:ignoreversion recursesubdirs createallsubdirs ;
;Source: String: {code:GetFacilityLogo} ; DestDir: {app};
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
[UninstallRun]
Filename: "{cmd}"; Parameters: "/C ""taskkill /im DicomConverter.exe /f /t"
Filename: "{cmd}"; Parameters: "/C ""taskkill /im dicom_converting_process.exe /f /t"