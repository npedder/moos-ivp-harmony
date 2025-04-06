/************************************************************/
/*    NAME: Simen Sem Oevereng                              */
/*    ORGN: MIT: 2.680 Spring 2019, http://oceanai.mit.edu  */
/*    FILE: ReturnSignal.h                                      */
/*    DATE: Feb 14, 2019                                    */
/*    EDIT: none  

      Implementations: ReturnSignal.cpp

      This file contains the declarations of lab 4, in 
      which the goal was to learn how to write a MOOSApp, 
      in order to interact with a MOOS mission, alder.moos.
      the app simply calculates the total travelled distance
      of a single vessel.      
      
/************************************************************/

#ifndef ReturnSignal_HEADER
#define ReturnSignal_HEADER

#include "MOOS/libMOOS/MOOSLib.h"
#include "MOOS/libMOOS/Thirdparty/AppCasting/AppCastingMOOSApp.h"
#include <string>

// inherits from AppCastingMOOSApp class to enable AppCasting
class ReturnSignal : public AppCastingMOOSApp
{
 public:
   ReturnSignal();
   ~ReturnSignal();

 protected: // Standard MOOSApp functions being overloaded 
   bool OnNewMail(MOOSMSG_LIST &NewMail);
   bool Iterate();
   bool OnConnectToServer();
   bool OnStartUp();
   bool buildReport();

 protected: // App-specific functions / parameters
   void RegisterVariables();           // Registers variables published to the community

   string m_community;
   bool m_received_return;
   bool m_received_community;

};

#endif 