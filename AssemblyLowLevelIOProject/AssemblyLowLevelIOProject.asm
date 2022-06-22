TITLE Designing Low Level Input Output Procedures

; Author: Samuel Haupt
; Project Number: Project #6         Due Date: 06/05/2022
; Description:  Program requests user to input 10 signed integers by recording
;       string representation of inputs. Converts string integers into 
;       signed integers and stores within an array. The conversion from string
;       to integer shifts according to ASCII table value and represents the value 
;       as hexidecimal at a low level. Tests input is valid by ensuring input
;       is within the required range (neg)2^31 to 2^31 sub 1 and does not contain
;       any improper characters that do not convert to an integer.
;       Finally, the program reverses functionality and converts back to string
;       before printing to console. Sum and truncated average are displayed also
;       using a procedure to print strings.

INCLUDE Irvine32.inc

; ---------------------------------------------------------------------------------
; Name: mGetString
;
; Description:  Macro awaits integer input from user. Saves it at address supplied and 
;       returns the number of characters received.
; Receives:   userPromptAddr = (input: reference) address of string array for user prompt.
;       userInputAddr = (output: reference) address for where to store user input.
;       userInputSize = (input: value) value of allowed user input size.
;       charCountReadAddr = (output: reference) address of variable that stores value of
;                 characters read from input.
; returns:    Global variables are changed: userInput stored at userInputAddr and 
;                       charCountRead stored at charCountReadAddr.
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
; Description:  Macro for writing a string-converted integer to the console.
; Preconditions:  Must receive address of string array.
; Receives:   asciiConvertedToStrAddr = address of string array (input: address).
; returns:    None.
; ---------------------------------------------------------------------------------
mDisplayString MACRO asciiConvertedToStrAddr:REQ
  PUSH  EDX

  MOV EDX, asciiConvertedToStrAddr
  CALL  WriteString

  POP EDX
ENDM

FOUR_BYTES    = 4d
NEGATIVE_SYMBOL = 2Dh
POSITIVE_SYMBOL = 2Bh
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

finalNumbersTitle BYTE  "You entered the following numbers: ",13,10,0
sumOfNumbersTitle BYTE  "The sum of these numbers is: ",0
sumOfNumbers    SDWORD  0
truncAverageTitle BYTE  "The truncated average is: ",0
truncAverage    SDWORD  0
goodbyeMessage    BYTE  "Come again!",13,10,0

.code
main PROC

  PUSH  OFFSET intro3
  PUSH  OFFSET intro2
  PUSH  OFFSET intro1
  PUSH  OFFSET introTitle
  CALL  Introduction

;-----------------------------------
; Loops through and reads user's input 10x.
; Displays error message if input is invalid.
; Stores in userArray when input is valid.
;-----------------------------------
  MOV ECX, 10
  MOV EBX, 0
_ReadValLoop:
  MOV userInputSignedInt, 0
  PUSH  OFFSET charCountRead
  PUSH  OFFSET userInputSignedInt
  PUSH  userInputSize
  PUSH  OFFSET userInput
  PUSH  OFFSET userPrompt
  CALL  ReadVal
  
;Check if user input is valid.
  CMP EAX, 1              
  JNE _InvalidInput
  DEC ECX
 

; Stores user input into userArray.
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

;-----------------------------------
; Loops through and writes 10 elements from array.
;-----------------------------------
  CALL  CrLf
  MOV EDX, OFFSET finalNumbersTitle
  CALL  WriteString

  MOV ESI, OFFSET userArray
  MOV ECX, 9
_WriteValLOOP:
  PUSH  [ESI]
  CALL  WriteVal
  MOV EDX, OFFSET commaSpace
  CALL  WriteString
  ADD ESI, FOUR_BYTES
  LOOP  _WriteValLOOP
  PUSH  [ESI] 
  CALL  WriteVal
  CALL  CrLf
  CALL  CrLf


  PUSH  OFFSET truncAverage
  PUSH  OFFSET sumOfNumbers
  PUSH  OFFSET userArray
  CALL  CalculateSumAndAverage
  
  PUSH  truncAverage
  PUSH  OFFSET truncAverageTitle
  PUSH  sumOfNumbers
  PUSH  OFFSET sumOfNumbersTitle
  CALL  DisplaySumAndAverage
  
  MOV EDX, OFFSET goodbyeMessage
  CALL  WriteString
  CALL  CrLf

  Invoke ExitProcess,0  ; exit to operating system
main ENDP

; ---------------------------------------------------------------------------------
; Name: Introduction
;
; Description:  Displays programmer's name and program's title. Displays description of
;       program. Calls WriteString.
; Preconditions:  Must pass four variables by reference.
; Receives:   [EBP + 20] = intro title and programmer (input: value).
;       [EBP + 16] = intro 1 (input: value).
;       [EBP + 12] = intro 2 (input: value).
;       [EBP + 8]  = intro 3 (input: value).
;       FOUR_BYTES global constant that provides the constant value 4.
; returns:    None.
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
; Description:  Requests user to input signed integer. Uses mGetString to read in the value.
;       Detects if input contains symbol prefix (positive or negative) and if input
;       is within required length. Applies an ASCII shift to match a number value.
;       Sets EAX register to 1 or 0 to indicate user request was valid or not 
;       valid (respectively). Calls CrLF.
; Preconditions:  Data type needs to be signed/unsigned integer. Do not use EAX register.
; Postconditions: EAX register is changed.
; Receives:   [EBP + 8]   = (input: reference) address of userInputPrompt.
;       [EBP + 12]  = (output: reference) address of userInput.
;       [EBP + 16]  = (input: value) userInputSize value that is allowed for user input.
;       [EBP + 20]  = (output: reference) address of userInputSignedInt.
;       [EBP + 24]  = (output: reference) address of charCountRead.
;       ASCII_SHIFT = 48d
;       ZERO    = 30h
;       NINE    = 39h
;       NEGATIVE_SYMBOL = 2Dh
;       POSITIVE_SYMBOL = 2Bh
;       TEN_SHIFT   = 10d
;       FOUR_BYTES  = 4d
; returns:    EAX holds a boolean: true (1) or false (0).
; ---------------------------------------------------------------------------------
ReadVal PROC
  LOCAL userInputAddr:DWORD
  LOCAL userInputLength:DWORD
  LOCAL inputSignedIntAddr:SDWORD
  LOCAL charCountAddr:DWORD
  LOCAL charCount:DWORD
  LOCAL signSymbol:BYTE
  LOCAL shiftedValue:SDWORD
  LOCAL savedInteger:SDWORD

  PUSH  EBX
  PUSH  ECX
  PUSH  EDX
  PUSH  EDI
  PUSH  ESI

;---------------------------
; Set up local variables with passed
; parameters.
;---------------------------
  MOV EBX, [EBP + 3*FOUR_BYTES]
  MOV userInputAddr, EBX
  MOV EBX, [EBP + 4*FOUR_BYTES]
  MOV userInputLength, EBX
  MOV EBX, [EBP + 5*FOUR_BYTES]
  MOV inputSignedIntAddr, EBX
  MOV EBX, [EBP + 6*FOUR_BYTES]
  MOV charCountAddr, EBX

  mGetString [EBP + 2*FOUR_BYTES], userInputAddr, userInputLength, charCountAddr
  
;----------------------------
; Sets source and destination registers
; and detects if input contains a sign symbol.
;----------------------------
  MOV EBX, charCountAddr
  MOV EAX, [EBX]
  MOV charCount, EAX

  MOV signSymbol, 0
  MOV EDI, inputSignedIntAddr
  MOV EBX, [EDI]
  MOV savedInteger, EBX
  MOV ESI, userInputAddr
  MOV BL, BYTE PTR [ESI]
  CMP BL, NEGATIVE_SYMBOL
  JNE _DoNotSetNegativeSignSymbol
  MOV signSymbol, NEGATIVE_SYMBOL
_DoNotSetNegativeSignSymbol:
  CMP BL, POSITIVE_SYMBOL
  JNE _DoNotSetPositiveSignSymbol
  MOV signSymbol, POSITIVE_SYMBOL
_DoNotSetPositiveSignSymbol:

;-----------------------------
; Establish if user input is within required length,
; including an input with symbol prefix.
;-----------------------------
  CMP signSymbol, 0
  JE  _InputDoesNotHavePrefix
  MOV EBX, charCount
  CMP EBX, 11
  JG  _InputIsNotValid
  JMP _InputWithinRange
_InputDoesNotHavePrefix:
  MOV EBX, charCount
  CMP EBX, 10
  JG  _InputIsNotValid
  JMP _InputWithinRange

;-----------------------------
; Sets registers to loop over string array.
; Decrementing if sign symbol included in user input.
;-----------------------------
_InputWithinRange:  
  MOV ECX, charCount
  CMP signSymbol, 0
  JE  _ConvertToIntegerLOOP
  INC ESI       
  DEC ECX
_ConvertToIntegerLOOP:
  XOR EAX, EAX
  CLD
  LODSB
  CMP   AL, ZERO
  JL    _InputIsNotValid
  CMP   AL, NINE
  JG    _InputIsNotValid

  SUB   AL, ASCII_SHIFT
  CMP   signSymbol, NEGATIVE_SYMBOL
  JNE   _DoNotNegateShiftedValue
  NEG   EAX
  _DoNotNegateShiftedValue:
  MOV   shiftedValue, EAX

  MOV   EAX, savedInteger     
  MOV   EDX, TEN_SHIFT
  IMUL  EDX
  ADD   EAX, shiftedValue
  JO    _InputIsNotValid        ; Detects boundaries: (neg)2^31 & 2^31 minus 1
  MOV   savedInteger, EAX
  MOV   [EDI], EAX
  LOOP  _ConvertToIntegerLOOP
  JMP _InputIsValid

;-----------------------------
; Sets EAX register to 1 if input is valid
; and passed back to calling procedure.
; Otherwise, EAX is set to 0.
;-----------------------------
_InputIsValid:
  MOV EAX, 1
  JMP _FinishedReadVal
_InputIsNotValid:
  MOV EAX, 0
_FinishedReadVal:

  POP ESI
  POP EDI
  POP EDX
  POP ECX
  POP EBX
  
  RET 5*FOUR_BYTES
ReadVal ENDP

; ---------------------------------------------------------------------------------
; Name: WriteVal
;
; Description:  Converts signed integer to ASCII byte string and writes to console.  
;       Calls DigitsCount for the total number of characters needed for  
;       string conversion. Sets the front of string array with negative symbol
;       and zero at the end of array for null-termination. Divides by 10 to
;       obtain the least significant digit and converts this value by shifting
;       with the constant ASCII_SHIFT. Uses mDisplayString to write ASCII version
;       of the signed integer.
; Preconditions:  Data type needs to be signed/unsigned integer.
; Receives:   [EBP + 8]   = indexed signed integer (input: value).
;       ASCII_SHIFT = 48d
;       NEGATIVE_SYMBOL = 2Dh
;       TEN_SHIFT   = 10d
;       FOUR_BYTES  = 4d
; returns:    None.
; ---------------------------------------------------------------------------------
WriteVal PROC
  LOCAL remainingIntegerVal:DWORD
  LOCAL negativeSymbol:BYTE
  LOCAL asciiConvertedToStr[12]:BYTE

  PUSH  EAX
  PUSH  EBX
  PUSH  ECX
  PUSH  EDX
  PUSH  EDI
  PUSH  ESI

;---------------------------
; Set local variables with passed parameter, sets negative symbol,
; and retrieves character count from DigitsCount procedure.
;---------------------------
  MOV EAX, [EBP + 2*FOUR_BYTES]
  MOV remainingIntegerVal, EAX
  MOV negativeSymbol, 0
  CMP EAX, 0
  JNS _DoNotSetNegativeSymbol
  MOV negativeSymbol, NEGATIVE_SYMBOL
_DoNotSetNegativeSymbol:
  
  MOV EAX, DWORD PTR negativeSymbol
  PUSH  EAX
  PUSH  remainingIntegerVal
  CALL  DigitsCount

;---------------------------
; Load negative symbol to string array and
; set null-termination in string array.
;---------------------------
  LEA EDI, asciiConvertedToStr
  MOV AL, negativeSymbol
  CLD
  STOSB

  LEA EDI, asciiConvertedToStr  
  ADD EDI, ECX
  MOV AL, 0
  STD
  STOSB                 
  MOV EBX, TEN_SHIFT

_ConvertToAsciiLOOP:
  MOV EAX, remainingIntegerVal
  CDQ
  IDIV  EBX
  MOV remainingIntegerVal, EAX

  CMP negativeSymbol, NEGATIVE_SYMBOL   ; Handles negative signed integers.
  JNE _SkipNegationBeforeAsciiShift
  NEG EDX
  _SkipNegationBeforeAsciiShift:

  MOV AL, DL
  ADD AL, ASCII_SHIFT
  STD
  STOSB

  CMP negativeSymbol, NEGATIVE_SYMBOL
  JNE _ContinueAsciiLOOP

  CMP ECX, 2
  JNE _ContinueAsciiLOOP
  DEC ECX                 ; Stops the conversion due to negative symbol at front.

  _ContinueAsciiLOOP:
  LOOP  _ConvertToAsciiLOOP

  LEA ESI, asciiConvertedToStr
  mDisplayString ESI

  POP ESI
  POP EDI
  POP EDX
  POP ECX
  POP EBX
  POP EAX

  RET 1*FOUR_BYTES
WriteVal ENDP

; ---------------------------------------------------------------------------------
; Name: DigitsCount
;
; Description:  Counts the number of character digits, including the negative symbol,
;       and returns count in ECX register. Uses TEN_SHIFT to divide out each 
;       digit until quotient reaches 0.
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

;---------------------------
; Set up local variables with passed
; parameters.
;---------------------------
  MOV EAX, [EBP + 2*FOUR_BYTES]
  MOV integerToCount, EAX
  MOV EBX, [EBP + 3*FOUR_BYTES]
  MOV negativeSymbol, BL
  MOV charCount, 0

  
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

; ---------------------------------------------------------------------------------
; Name: CalculateSumAndAverage
;
; Description:  Calculate sum of 10 elements in array and stores in sumOfNumbers variable.
;       Then calculates an average of those 10 elements and truncates to an integer.
; Preconditions:  Requires array to hold signed/unsigned integers.
; Receives:   [EBP + 8]  = userArray address (input: parameter).
;       [EBP + 12] = sumOfNumbers address (output: parameter).
;       [EBP + 16] = truncAverage address (output: parameter).
;       FOUR_BYTES global constant that provides the constant value 4.
; returns:    sumOfNumbers and truncAverage are filled with sum and average values.
; ---------------------------------------------------------------------------------
CalculateSumAndAverage PROC
  LOCAL userArrayAddr:DWORD
  LOCAL sumOfNumbersAddr:DWORD
  LOCAL truncAverageAddr:DWORD

  PUSH  EAX
  PUSH  EBX
  PUSH  ECX
  PUSH  EDI
  PUSH  ESI

;---------------------------
; Set up local variables with passed
; parameters.
;---------------------------
  MOV EBX, [EBP + 2*FOUR_BYTES]
  MOV userArrayAddr, EBX
  MOV EBX, [EBP + 3*FOUR_BYTES]
  MOV sumOfNumbersAddr, EBX
  MOV EBX, [EBP + 4*FOUR_BYTES]
  MOV truncAverageAddr, EBX

  MOV ESI, userArrayAddr
  MOV ECX, 10
  XOR EAX, EAX
_CalculateSumLOOP:
  MOV EBX, [ESI]
  ADD EAX, EBX
  ADD ESI, FOUR_BYTES
  LOOP  _CalculateSumLOOP

  MOV EDI, sumOfNumbersAddr
  MOV [EDI], EAX

  CDQ
  MOV EBX, 10
  IDIV  EBX

  MOV EDI, truncAverageAddr
  MOV [EDI], EAX

  POP ESI
  POP EDI
  POP ECX
  POP EBX
  POP EAX

  RET 3*FOUR_BYTES

CalculateSumAndAverage ENDP

; ---------------------------------------------------------------------------------
; Name: DisplaySumAndAverage
;
; Description:  Display sum and average titles, and also display sum and average
;       of 10 elements in user array.
; Receives:   [EBP + 8] = sumOfNumbersTitle address (input: parameter).
;       [EBP + 12] = sumOfNumbers address (input: parameter).
;       [EBP + 16] = truncAverageTitle address (input: parameter).
;       [EBP + 20] = truncAverage address (input: parameter).
;       FOUR_BYTES global constant that provides the constant value 4.
; returns:    None.
; ---------------------------------------------------------------------------------
DisplaySumAndAverage PROC
  LOCAL sumOfNumbersTitleAddr:DWORD
  LOCAL sumOfNumbersAddr:DWORD
  LOCAL truncAverageTitleAddr:DWORD
  LOCAL truncAverageAddr:DWORD

  PUSH  EAX
  PUSH  EBX
  PUSH  EDX
  PUSH  ESI

;---------------------------
; Set up local variables with passed
; parameters.
;---------------------------
  MOV EBX, [EBP + 2*FOUR_BYTES]
  MOV sumOfNumbersTitleAddr, EBX
  MOV EBX, [EBP + 3*FOUR_BYTES]
  MOV sumOfNumbersAddr, EBX
  MOV EBX, [EBP + 4*FOUR_BYTES]
  MOV truncAverageTitleAddr, EBX
  MOV EBX, [EBP + 5*FOUR_BYTES]
  MOV truncAverageAddr, EBX

  MOV EDX, sumOfNumbersTitleAddr
  CALL  WriteString

  LEA ESI, sumOfNumbersAddr
  PUSH  [ESI]
  CALL  WriteVal
  CALL  CrLf

  MOV EDX, truncAverageTitleAddr
  CALL  WriteString

  LEA ESI, truncAverageAddr
  PUSH  [ESI]
  CALL  WriteVal

  CALL  CrLf
  CALL  CrLf

  POP ESI
  POP EDX
  POP EBX
  POP EAX

  RET 4*FOUR_BYTES

DisplaySumAndAverage ENDP

END main
