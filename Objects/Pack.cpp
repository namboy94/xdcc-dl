/*
 * @author Hermann Krumrey <hermann@krumreyh.com>
 */

#include "ServerList.h"

//public
//Constructor

/**
 * Creates a new Pack object with a given pack number
 * @param packNumber - the number of the pack
 */
Pack::Pack(int packNumber) {

    this->packNumber = packNumber;

}

//getter/setter

string Pack::getPackNumberString() {
    return to_string(this->packNumber);
}