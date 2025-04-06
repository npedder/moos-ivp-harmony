#--------------------------------------------------------
# The CMakeLists.txt for:                       pReturnSignal
# Author(s):                              Simen Sem Oevereng
#--------------------------------------------------------

SET(SRC
  ReturnSignal.cpp
  ReturnSignal_Info.cpp
  main.cpp
)

ADD_EXECUTABLE(pReturnSignal ${SRC})

TARGET_LINK_LIBRARIES(pReturnSignal
   ${MOOS_LIBRARIES}
   mbutil
   m
   pthread)

