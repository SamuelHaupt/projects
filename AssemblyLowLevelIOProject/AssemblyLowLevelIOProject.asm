TITLE Designing Low Level Input Output Procedures     (Proj6_hauptsa.asm)

; Author: Samuel Haupt
; Last Modified: 05/27/2022
; Course number/section: Oregon State Uni:   CS271 Section 400
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
mGetString MACRO userPromptAddr:REQ, userInputAddr:REQ, userInputSize:REQ, charCount:REQ
  PUSH  EAX
  PUSH  ECX
  PUSH  EDX

  MOV EDX, userPromptAddr
  CALL  WriteString

  MOV EDX, userInputAddr
  MOV ECX, userInputSize
  CALL  ReadString
  MOV charCount, EAX

  POP EDX
  POP ECX
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
mGDisplayString MACRO userPromptAddr:REQ, userInputAddr:REQ, userInputSize:REQ, charCount:REQ
  PUSH  EAX
  PUSH  ECX
  PUSH  EDX

  MOV EDX, userPromptAddr
  CALL  WriteString

  MOV EDX, userInputAddr
  MOV ECX, userInputSize
  CALL  ReadString
  MOV charCount, EAX

  POP EDX
  POP ECX
  POP EAX
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
userInputSignedInt  SDWORD  0
userPromptError   BYTE  "ERROR: You did not enter a signed number or your number was too big.",13,10,0

.code
main PROC

  PUSH  OFFSET intro3
  PUSH  OFFSET intro2
  PUSH  OFFSET intro1
  PUSH  OFFSET introTitle
  CALL  introduction

  MOV ECX, 10

_ReadValLoop:
  PUSH  ECX
  MOV userInputSignedInt, 0
  PUSH  OFFSET userInputSignedInt
  PUSH  userInputSize
  PUSH  OFFSET userInput
  PUSH  OFFSET userPrompt
  CALL  readVal
  POP ECX
  ;----
  ;clear
  ;----
  PUSH  EAX
  MOV EAX, userInputSignedInt
  CALL  WriteInt
  CALL  CrLf
  POP EAX
  
  CMP EAX, 1
  JNE _InvalidInput
  DEC ECX
  JMP _ValidInput
  _InvalidInput:
  MOV EDX, OFFSET userPromptError
  CALL  WriteString
  _ValidInput:
  CMP ECX, 0
  JG  _ReadValLoop

  Invoke ExitProcess,0  ; exit to operating system
main ENDP

; ---------------------------------------------------------------------------------
; Name: introduction
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
introduction PROC
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
introduction ENDP

; ---------------------------------------------------------------------------------
; Name: readVal
;
; Description:  Displays prog
; Preconditions:  userPrompt needs to be on stack at EBP + 8.
; Postconditions: None.
; Receives:   userPrompt (input) offset that references the starting point of the variable.
;       FOUR_BYTES global constant that provides the constant value 4.
; returns:    No parameters or global constants are changed.
; ---------------------------------------------------------------------------------
readVal PROC
  LOCAL charCount:DWORD
  LOCAL negativeSymbol:BYTE

  PUSH  EAX
  PUSH  EBX
  PUSH  ECX
  PUSH  EDX
  PUSH  ESI

  mGetString [EBP + 2*FOUR_BYTES], [EBP + 3*FOUR_BYTES], [EBP + 4*FOUR_BYTES], charCount

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
  MOV EBX, charCount
  CMP EBX, 11
  JG  _IsNotValidInput
  JMP _InputWithinRange
_NotNegativeInput:
  MOV EBX, charCount
  CMP EBX, 10
  JG  _IsNotValidInput

_InputWithinRange:
  CLD 
  MOV ECX, charCount  ;only for positive
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
  
;Test border case: -2147483648
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

;Test border case: 2147483647
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
  JMP _FinishReadVal
_IsNotValidInput:
  MOV EAX, 0
_FinishReadVal:

  POP ESI
  POP EDX
  POP ECX
  POP EBX
  ;POP  EAX   ;returns EAX with boolean
  
  RET 4*FOUR_BYTES
readVal ENDP

END main
