/************************************************************/
/*    NAME: Simen Sem Oevereng                              */
/*    ORGN: MIT: 2.680 Spring 2019, http://oceanai.mit.edu  */
/*    FILE: ReturnSignal.cpp                                    */
/*    DATE: Feb 14, 2019                                    */
/*    EDIT: none  

      This file contains the implementation of lab 4, in 
      which the goal was to learn how to write a MOOSApp, 
      in order to interact with a MOOS mission, alder.moos.
      the app simply calculates the total travelled distance
      of a single vessel.
      
/************************************************************/

#include <iterator>
#include "MBUtils.h"
#include "ReturnSignal.h" // declaration
#include <math.h>     // for sqrt() procedure
#include <string>

using namespace std;

//---------------------------------------------------------
// Constructor

ReturnSignal::ReturnSignal()
{
  // positions and distances
   m_received_return = false;
}

//---------------------------------------------------------
// Destructor

ReturnSignal::~ReturnSignal()
{
  // No dynamically allocated variables to delete yet
}

//---------------------------------------------------------
// Procedure: OnNewMail
// PURPOSE:   react to subscribed mails sent from (preferably) another MOOSApp 
// @param     NewMail: a MOOSMSG_LIST type variable,
//				containing all information published from other MOOSApps
// @edits     m_current_x, m_current_y, m_first_reading
// @return    true
bool ReturnSignal::OnNewMail(MOOSMSG_LIST &NewMail)
{
  AppCastingMOOSApp::OnNewMail(NewMail);

  // Iterate through all mail
  MOOSMSG_LIST::iterator p;
  for(p=NewMail.begin(); p!=NewMail.end(); p++) {
    CMOOSMsg &msg = *p;

    string key = msg.GetKey();        // Gets variable name
    string value = msg.GetString();

    // Checks explicitly for variablename we are interested in
    if (key == "RETURN"){
      if (value == "true"){
      m_community_name = msg.GetCommunity(); // or msg.GetDouble() depending on use
      m_received_return = true;
      }
    else if(value == "false"){
      m_received_return = false;
    }
    }
  }
   return(true);
}

//---------------------------------------------------------
// Procedure: OnConnectToServer
// PURPOSE:   ---
// @param     no inputs
// @edits     no edits
// @returns   true

bool ReturnSignal::OnConnectToServer()
{	
   RegisterVariables();
   return(true);
}

//---------------------------------------------------------
// Procedure: Iterate()
//            happens AppTick times per second
// PURPOSE:   contains the main logic of the MOOSApp
// @param     no inputs
// @edits     m_total_distance
// @returns

bool ReturnSignal::Iterate()
{
  // Calling Iterate() from parent class to enable casting
  AppCastingMOOSApp::Iterate();

  if(m_received_return)
    {
      std::string status_msg = "NAME=" + m_community_name + ",STATUS=3";
      Notify("STATUS", status_msg);
    }

  AppCastingMOOSApp::PostReport(); // posts to AppCast: variable(s) specified in ReturnSignal::buildReport()
  return(true);
}

//---------------------------------------------------------
// Procedure: OnStartUp()
//            virtual function
//            happens before connection is open
// PURPOSE:   grabbing configuration parameters relevant for the given app
// @param     no inputs
// @edits     no edits
// @returns   true

bool ReturnSignal::OnStartUp()
{
  AppCastingMOOSApp::OnStartUp();

  // Collects list of parameters from .moos file
  // Since we register hardcode variable names, this loop is not necessary, but is kept for later reference
  list<string> sParams;
  m_MissionReader.EnableVerbatimQuoting(false);
  if(m_MissionReader.GetConfiguration(GetAppName(), sParams)) {
    
    list<string>::iterator p;
    for(p=sParams.begin(); p!=sParams.end(); p++) {
      string line  = *p;
      string param = biteStringX(line, '=');
      string value = line;
    }

  }
  
  // Calls function in the end for registering variables to subscribe to relevant mail
  RegisterVariables();	
  return(true);
}

//---------------------------------------------------------
// Procedure:   RegisterVariables
// PURPOSE:     selects variables to register 
// @param       no inputs
// @edits       no edits
// @returns     nothing
void ReturnSignal::RegisterVariables()
{
  // Calling function defined in parent class AppCastingMOOSApp
  AppCastingMOOSApp::RegisterVariables();

  // Explicitly register for the MOOS-variables we want
  Register("RETURN", 0); // second parameter == 0 as we would like every update
}

//---------------------------------------------------------
// Procedure: buildReport
// PURPOSE:   prints selected values to AppCastingMOOSApp
// @param     no inputs
// @edits     member variable m_msgs
// @returns   true
bool ReturnSignal::buildReport()
{
  // Sending string and variable value to m_msgs: the output stream of the casting application
  m_msgs << "RETURNED: " << (m_received_return ? "true" : "false") << endl;

  return(true);
}