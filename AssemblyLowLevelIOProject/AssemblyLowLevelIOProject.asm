TITLE Designing Low Level Input Output Procedures     (Proj6_hauptsa.asm)

; Author: Samuel Haupt
; Last Modified: 05/25/2022
; Course number/section:   CS271 Section 400
; Project Number: Project 6         Due Date: 06/05/2022
; Description: COMMMMMMMMPPPPPPPLLLLLLLLLLEEEEEETTTTTTTTEEEEEEEE

INCLUDE Irvine32.inc

; ---------------------------------------------------------------------------------
; Name: mGetString
;
; Description:  Calls ReadString and saves inputted value to userInput.
; Preconditions:  Don't use EAX, ECX, and EDX as arguments.
; Postconditions: None.
; Receives:   userInput (output) local variable to input user input.
; returns:    userInput is changed and filled with user input.
; ---------------------------------------------------------------------------------
mGetString MACRO userPromptAddr:REQ, userInputAddr:REQ, userInputSize:REQ, charCountReadAddr:REQ
  PUSH  EAX
  PUSH  EBX
  PUSH  ECX
  PUSH  EDX

  MOV EDX, userPromptAddr
  CALL  WriteString

  MOV EDX, userInputAddr
  MOV ECX, userInputSize
  CALL  ReadString
  MOV EBX, charCountReadAddr
  MOV [EBX], EAX

  POP EDX
  POP ECX
  POP EBX
  POP EAX
ENDM

; ---------------------------------------------------------------------------------
; Name: mDisplayString
;
; Description:  
; Preconditions:  
; Postconditions: None.
; Receives:   
; returns:    
; ---------------------------------------------------------------------------------
mDisplayString MACRO stringifiedNumericalValueAddr:REQ
  PUSH  EDX

  MOV EDX, stringifiedNumericalValueAddr
  CALL  WriteString

  POP EDX
ENDM


FOUR_BYTES    = 4d
NEGATIVE_SYMBOL = 2Dh
ZERO      = 30h
NINE      = 39h
ASCII_SHIFT   = 48d
TEN_SHIFT   = 10d

.data

introTitle      BYTE  "Designing Low-Level I/O Procedures Program by Samuel Haupt.",13,10,0
intro1        BYTE  "Please provide 10 signed decimal integers.",13,10,0
intro2        BYTE  "Each number needs to be small enough to fit inside a 32 bit register. After you have finished inputting",13,10,0
intro3        BYTE  "the raw numbers I will display a list of the integers, their sum, and their average value.",13,10,0

userPrompt      BYTE  "Please enter an signed number: ",0
userInput     BYTE  33 DUP(?)
userInputSize   DWORD SIZEOF userInput
charCountRead   DWORD ?
userInputSignedInt  SDWORD  0
userPromptError   BYTE  "ERROR: You did not enter a signed number or your number was too big.",13,10,0

userArray     SDWORD  10 DUP(?)
commaSpace      BYTE  ", ",0

.code
main PROC

  PUSH  OFFSET intro3
  PUSH  OFFSET intro2
  PUSH  OFFSET intro1
  PUSH  OFFSET introTitle
  CALL  Introduction

  MOV ECX, 10
  MOV EBX, 0

_ReadValLoop:
  PUSH  ECX
  MOV userInputSignedInt, 0
  PUSH  OFFSET charCountRead
  PUSH  OFFSET userInputSignedInt
  PUSH  userInputSize
  PUSH  OFFSET userInput
  PUSH  OFFSET userPrompt
  CALL  ReadVal
  POP ECX
  
  CMP EAX, 1    ;ReadVal returns EAX changed
  JNE _InvalidInput
  DEC ECX

  MOV EAX, userInputSignedInt
  MOV EDI, OFFSET userArray
  MOV [EDI + EBX*FOUR_BYTES], EAX
  INC EBX
  JMP _ValidInput

  _InvalidInput:
  MOV EDX, OFFSET userPromptError
  CALL  WriteString
  _ValidInput:
  CMP ECX, 0
  JG  _ReadValLoop

  MOV ESI, OFFSET userArray
  MOV ECX, 9

_WriteValLOOP:
  
  
  PUSH  charCountRead
  PUSH  ESI   ;OFFSET OF ARRAY //// push value only
  CALL  WriteVal

  MOV EDX, OFFSET commaSpace
  CALL  WriteString
  ADD ESI, FOUR_BYTES
  LOOP  _WriteValLOOP
  
  PUSH  ESI   
  CALL  WriteVal
  

  Invoke ExitProcess,0  ; exit to operating system
main ENDP

; ---------------------------------------------------------------------------------
; Name: Introduction
;
; Description:  Displays programmer's name and program's title. Displays description of
;       program. Calls WriteString.
; Preconditions:  
;         introTitle needs to be on stack at EBP + 20.
;         intro3 needs to be on stack at EBP + 16.
;         intro2 needs to be on stack at EBP + 12.
;         intro1 needs to be on stack at EBP + 8.
; Postconditions: None.
; Receives:   introTitle (input) offset that references the starting point of the variable.
;       intro1 (input) offset that references the starting point of the variable.
;       intro2 (input) offset that references the starting point of the variable.
;       intro3 (input) offset that references the starting point of the variable.
;       FOUR_BYTES global constant that provides the constant value 4.
; returns:    No parameters or global constants are changed.
; ---------------------------------------------------------------------------------
Introduction PROC
  PUSH  EBP
  MOV   EBP, ESP

  PUSH  EDX

  MOV EDX, [EBP + 2*FOUR_BYTES]
  CALL  WriteString  
  CALL  CrLf
  
  MOV EDX, [EBP + 3*FOUR_BYTES]
  CALL  WriteString
  MOV EDX, [EBP + 4*FOUR_BYTES]
  CALL  WriteString
  MOV EDX, [EBP + 5*FOUR_BYTES]
  CALL  WriteString
  CALL  CrLf
  CALL  CrLf

  POP EDX
  
  MOV   ESP, EBP
  POP EBP
  RET 4*FOUR_BYTES
Introduction ENDP

; ---------------------------------------------------------------------------------
; Name: ReadVal
;
; Description:  Displays prog
; Preconditions:  userPrompt needs to be on stack at EBP + 8.
; Postconditions: None.
; Receives:   userPrompt (input) offset that references the starting point of the variable.
;       FOUR_BYTES global constant that provides the constant value 4.
; returns:    No parameters or global constants are changed.
; ---------------------------------------------------------------------------------
ReadVal PROC
  LOCAL negativeSymbol:BYTE
  LOCAL charCountLOCAL:DWORD

  PUSH  EAX
  PUSH  EBX
  PUSH  ECX
  PUSH  EDX
  PUSH  ESI

  mGetString [EBP + 2*FOUR_BYTES], [EBP + 3*FOUR_BYTES], [EBP + 4*FOUR_BYTES], [EBP + 6*FOUR_BYTES]

  MOV EBX, [EBP + 6*FOUR_BYTES]
  MOV EAX, [EBX]
  MOV charCountLOCAL, EAX
  MOV EDX, [EBP + 3*FOUR_BYTES]
  CALL  WriteString
  CALL  CrLf
  
;----------------------------
; Validator. Sets EAX to 0 if invlad input.
;      Otherwise, sets to 1.
;----------------------------
  MOV ESI, [EBP + 3*FOUR_BYTES]
  MOV BL, BYTE PTR [ESI]
  MOV negativeSymbol, BL
  CMP BL, NEGATIVE_SYMBOL
  JNE _NotNegativeInput
  MOV EBX, charCountLOCAL
  CMP EBX, 11
  JG  _IsNotValidInput
  JMP _InputWithinRange
_NotNegativeInput:
  MOV EBX, charCountLOCAL
  CMP EBX, 10
  JG  _IsNotValidInput

_InputWithinRange:
  CLD 
  MOV ECX, charCountLOCAL ;only for positive
  MOV BL, negativeSymbol
  CMP BL, NEGATIVE_SYMBOL
  JNE _ConvertToSignedIntLOOP
  INC ESI       ;Removes negative symbol from string
  DEC ECX
_ConvertToSignedIntLOOP:
  XOR EAX, EAX
  LODSB
  CMP   AL, ZERO
  JL    _IsNotValidInput
  CMP   AL, NINE
  JG    _IsNotValidInput

  SUB   AL, ASCII_SHIFT
  MOV   EBX, EAX

  PUSH  EBX
  MOV   EBX, [EBP + 5*FOUR_BYTES]
  MOV   EAX, [EBX]
  POP   EBX

  MOV   EDX, TEN_SHIFT
  MUL   EDX
  ADD   EAX, EBX
  MOV   EBX, [EBP + 5*FOUR_BYTES]
  MOV   [EBX], EAX
  JO    _PotentiallyInvalidInput
  LOOP  _ConvertToSignedIntLOOP

_PotentiallyInvalidInput:
  MOV BL, negativeSymbol
  CMP BL, NEGATIVE_SYMBOL
  JNE _DoNotNegate
  
;Test for border case: -2147483648 (-2^31)
  TEST  AL, AL
  MOV EBX, [EBP + 5*FOUR_BYTES]
  MOV EAX, [EBX]
  DEC EAX         ;value is positive
  TEST  AL, AL
  NEG EAX       
  JO  _IsNotValidInput
  DEC EAX
  MOV [EBX], EAX
  JMP _IsValidInput

;Test for border case: 2147483647 (2^31 -1)
_DoNotNegate:  
  TEST  AL, AL
  MOV EBX, [EBP + 5*FOUR_BYTES]
  MOV EAX, [EBX]
  DEC EAX
  JO  _IsNotValidInput
  INC EAX
  MOV [EBX], EAX
  JMP _IsValidInput

_IsValidInput:
  MOV EAX, 1
  JMP _FinishedReadVal
_IsNotValidInput:
  MOV EAX, 0
_FinishedReadVal:

  POP ESI
  POP EDX
  POP ECX
  POP EBX
  ;POP  EAX   ;returns EAX with boolean
  
  RET 5*FOUR_BYTES
ReadVal ENDP

; ---------------------------------------------------------------------------------
; Name: WriteVal
;
; Description:  Displays programmer's name and program's title. Displays description of
;       program. Calls WriteString.
; Preconditions:  
;         introTitle needs to be on stack at EBP + 20.
;         intro3 needs to be on stack at EBP + 16.
;         intro2 needs to be on stack at EBP + 12.
;         intro1 needs to be on stack at EBP + 8.
; Postconditions: None.
; Receives:   introTitle (input) offset that references the starting point of the variable.
;       intro1 (input) offset that references the starting point of the variable.
;       intro2 (input) offset that references the starting point of the variable.
;       intro3 (input) offset that references the starting point of the variable.
;       FOUR_BYTES global constant that provides the constant value 4.
; returns:    No parameters or global constants are changed.
; ---------------------------------------------------------------------------------
WriteVal PROC
  LOCAL remainingIntegerVal:DWORD
  LOCAL negativeSymbol:BYTE
  LOCAL asciiConvertedToStr[12]:BYTE

  PUSH  EAX
  PUSH  EBX
  PUSH  ECX
  PUSH  EDX
  PUSH  ESI

;Set up local variables.
  MOV EBX, [EBP + 2*FOUR_BYTES] ;pass address of array
  MOV EAX, [EBX]          ;Loaded Integer into EAX
  MOV remainingIntegerVal, EAX  ;saving value in local variable
  TEST  AL, AL
  CDQ               ;sign extend EAX into EDX. Sets SF/PL (sign) flag.
  MOV negativeSymbol, 0
  JNS _DoNotSetNegativeSymbol
  MOV negativeSymbol, NEGATIVE_SYMBOL
_DoNotSetNegativeSymbol:
  
  MOV EAX, DWORD PTR negativeSymbol
  PUSH  EAX
  PUSH  remainingIntegerVal
  CALL  DigitsCount


  MOV AL, 0
  MOV negativeSymbol, AL
  STD
  STOSB

  MOV EBX, [EBP + 2*FOUR_BYTES] ;pass address of array
  MOV EAX, [EBX]          ;Loaded Integer into EAX
  MOV remainingIntegerVal, EAX  ;saving value in local variable
  MOV EBX, TEN_SHIFT
  CMP EAX, 0
  JGE _IntegerNotNegative
  MOV AL, NEGATIVE_SYMBOL


_IntegerNotNegative:

_ConvertToAsciiLOOP:
  MOV EAX, remainingIntegerVal
  MOV EDX, 0
  IDIV  EBX
  MOV remainingIntegerVal, EAX

  MOV AL, DL
  ADD AL, ASCII_SHIFT
  STD
  STOSB

  LOOP  _ConvertToAsciiLOOP

  LEA EAX, asciiConvertedToStr
  mDisplayString EAX

  POP ESI
  POP EDX
  POP ECX
  POP EBX
  POP EAX

  RET 2*FOUR_BYTES
WriteVal ENDP

; ---------------------------------------------------------------------------------
; Name: DigitsCount
;
; Description:  Counts the number of character digits, including the negative symbol,
;       and returns count in ECX register.
; Preconditions:  Do not use ECX. Data type needs to be signed/unsigned integer.
; Postconditions: Changes ECX.
; Receives:   [EBP + 8]  = remainingIntegerVal (input: value).
;       [EBP + 12] = negativeSymbol (input: value).
;       TEN_SHIFT global constant that provides the constant value 10.
;       FOUR_BYTES global constant that provides the constant value 4.
; returns:    ECX contains the character count of integer.
; ---------------------------------------------------------------------------------
DigitsCount PROC
  LOCAL integerToCount:SDWORD
  LOCAL negativeSymbol:BYTE
  LOCAL charCount:DWORD

  PUSH  EAX
  PUSH  EBX
  PUSH  EDX

;Set up local variables.
  MOV EAX, [EBP + 2*FOUR_BYTES]
  MOV integerToCount, EAX
  MOV charCount, 0
  MOV EBX, [EBP + 3*FOUR_BYTES]
  MOV negativeSymbol, BL

  
  MOV AL, BYTE PTR charCount
  CMP AL, negativeSymbol
  JE  _NotNegativeDoNotIncCharCount
  INC charCount
_NotNegativeDoNotIncCharCount:
  MOV EBX, TEN_SHIFT
  MOV EAX, integerToCount

_CharCountLoop: 
  CDQ
  IDIV  EBX
  INC charCount
  CMP EAX, 0
  JNE _CharCountLoop

  MOV ECX, charCount

  POP EDX
  POP EBX
  POP EAX

  RET 2*FOUR_BYTES

DigitsCount ENDP

END main
