#SingleInstance, Force
#Include <convertHex>
#Include <JSON>
SendMode Input
SetWorkingDir, %A_ScriptDir%

SetBatchLines, -1

;; FileNames
fileName := "hexFinal_settings.txt"  ;; main text
hexFile := "settings.json"  ;; main text
; fileName := "hexFinal_controller.txt"  ;; controller text
; hexFile := "controls.json"  ;; controller text

;; Delete old hex dump
FileDelete, %fileName%

;; Mark FileRead operations as UTF-8
FileEncoding UTF-8

;; Read json file
FileRead, jsonData, %hexFile%
data := JSON.Load(jsonData)
hexFinal :=

for i, obj in data.1.strings
{
    ;; If en_string is blank, error out.
    if (obj.en_string == "")
    {
        MsgBox % obj.en_string . "has no value."
        ExitApp
    }

    ;; Convert utf-8 strings to hex
    jp := 00 . convertStrToHex(obj.jp_string)
    jp := RegExReplace(jp, "\r\n", "")
    jp_raw := obj.jp_string
    jp_len := StrLen(jp)

    en := 00 . convertStrToHex(obj.en_string)
    en := RegExReplace(en, "\r\n", "")
    en_raw := obj.en_string
    en_len := StrLen(en)

    ;; If the strings aren't exact, do stuff.
    if (jp_len != en_len)
    {
      ; If en_len is longer than the jp_len, we'll get stuck in an
      ; infinite loop until we OOM, so check this here.
      if (en_len > jp_len)
      {
          MsgBox String too long. Please fix and try again.`nJP string: %jp_raw%`nEN string: %en_raw%`n
          ExitApp
      }

      ;; Replace pipe character with line break
      if InStr(obj.jp_string, "|")
      {
          jp := StrReplace(jp, "7c", "0a")
          en := StrReplace(en, "7c", "0a")
      }

      ;; Add null term to end of jp string
      jp .= 00

      ;; Add null terms until the length of the en string
      ;; matches the jp string.
      Loop
      {
          en .= 00
          new_len := StrLen(en)
      }
      Until ((jp_len - new_len) == 0)
    }

    ;; Append hex value to var as we want one long string
    hexFinal .= en

    ;; When completed, output entire string to file
}

FileAppend, %hexFinal%, %fileName%