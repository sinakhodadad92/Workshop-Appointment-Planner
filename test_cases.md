### Updated Test Case Scenarios

#### **Appointment Class Tests**
1. **Test Appointment Creation with Valid Data**
2. **Test Appointment Creation with Invalid Date Format**
3. **Test Appointment Creation with Invalid Date (Today or Past Date)**
4. **Test Appointment Creation with Invalid Time Format**
5. **Test Equality of Two Appointments with Same ID**
6. **Test Inequality of Two Appointments with Different IDs**
7. **Test Appointment String Representation**
8. **Test Appointment Sorting by Date and Time**
9. **Test Emergency Appointment Flag Setting**
10. **Test Appointment Creation with Email**

#### **Scheduler Class Tests**
1. **Test Adding an Appointment within Opening Hours**
2. **Test Adding an Appointment Outside Opening Hours**
3. **Test Adding an Appointment During Lunch Break**
4. **Test Adding an Appointment in an Already Booked Time Slot**
5. **Test Adding an Appointment on a Date Before Tomorrow**
6. **Test Adding an Emergency Appointment Shifts Non-Emergency Appointment**
7. **Test Removing an Existing Appointment by ID**
8. **Test Removing a Non-Existing Appointment by ID**
9. **Test Editing an Appointment's Customer Name**
10. **Test Editing an Appointment's Date and Time to a Free Slot**
11. **Test Editing an Appointment's Date and Time to a Booked Slot**
12. **Test Listing Appointments for a Specific Date**
13. **Test Listing Free Time Slots for a Date**
14. **Test Listing Free Time Slots Excluding Lunch and Reserved Times**
15. **Test Sending Reminders for Appointments the Day Before**
16. **Test Sending Reminders with No Upcoming Appointments**
17. **Test Sending Instant Confirmation Email After Appointment Creation**
18. **Test Calculating Average Appointments per Day with Data**
19. **Test Calculating Average Appointments per Day with No Appointments**
20. **Test Handling of Emergency Appointments in Multiple Scenarios**

#### **FileHandler Class Tests**
1. **Test Saving Appointments to JSON File**
2. **Test Loading Appointments from JSON File**
3. **Test Handling of Non-Existent JSON File on Load**
4. **Test Handling of Corrupted JSON File on Load**
5. **Test Integrity of Data After Multiple Save and Load Cycles**

#### **Integration Tests**
1. **Test Full Workflow from Adding to Viewing Appointments**
2. **Test Workflow Including Editing and Deleting Appointments**
3. **Test Handling of Multiple Emergency Appointments in a Day**
4. **Test Performance with a Large Number of Appointments**
5. **Test Data Persistence Across Multiple Script Runs**
6. **Test User Interaction for Edge Cases (e.g., Invalid Inputs, Date Before Tomorrow)**
7. **Test System Behavior After Removing the JSON File**
8. **Test Sending Instant Confirmation Email and Reminders for Workflow**
