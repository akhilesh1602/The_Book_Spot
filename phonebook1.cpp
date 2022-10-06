#include<iostream>
#include <stdlib.h>
#include <string >
using namespace std;
struct node
{
   string name , number;
   node *next;
};
node *head = NULL , *newnode , *temp;
int len = 0 ;
void C_node ()
{
    newnode = new node;
    cout<<"Enter Name ";
    cin>>newnode->name;
    cout<<"Enter number ";
    cin>>newnode->number;
    newnode->next = NULL;
    if(head == NULL)
    {
        head = newnode;
        temp = newnode;
    }
    else
    {
        temp->next= newnode;
        temp = newnode;
    }
}
void display ()
{
    if(head == NULL)
    {
        cout<<"Contact list is Empty "<<endl;
    }
    else
    {
        node *trav = head ;
        while (trav != NULL)
        {
            cout<<"\n\t\tFull Name "<<trav->name<<endl;
            cout<<"\t\tPhone Number "<<trav->number<<endl;
            trav= trav->next;
            len++;
        }
        cout<<"Total contacts in the list = "<<len<<endl;
    }
}
void search_contact_delete () /// delete contact by name or phone number instead of index
{
    node *search_node = head, *next_node , *temp = head;
    ///*search_node pointer is used to find the contact
    ///*next_node pointer is used to free the deleted node storage

    string srch;
    int count = 0;
    cout<<"Enter your desired contact you want to search ";
    cin>>srch;
    bool found = false;
    if(head == NULL)
    {
        cout<<"\nList is Empty "<<endl;
    }
    else
    {
        while (search_node != NULL)
        {
            if(srch == search_node->name || srch == search_node->number)/// to search contact
            {
                if(count == 0) /// this will delete the first node
              {
              temp = head;
              head = head->next;
               delete temp;
              cout<<"\n\n\t\tContact has been deleted\n\n "<<endl;
    }


    ///in else part deletion at specific operation will perform
    else
    {
        for (int i = 1 ; i<count ; i++)///count will be the deleted contact position
        {
                temp= temp->next;

        }
        next_node = temp->next;
       temp->next = next_node->next;
        delete next_node;
        cout<<"\n\n\t\tContact has been deleted\n\n"<<endl;
    }


        found =true;
        break;
        }

             ///it will help while loop to continue until last node become
            search_node = search_node->next;
             count++;

        }
    }
    if(found == true)
    {

        cout<<"\t\tIndex of the Contact = "<<count+1<<endl;
    }
    else
    {
        cout<<"\n\t\tDesired contact not fount "<<endl;
    }
}

void clear_all ()
{
    if(head == NULL)
    {
        cout<<"List is Empty "<<endl;
    }
    else
    {
        temp = head ;
        while (head != NULL)
        {
            head = head->next;
            delete temp;
        }
        cout<<"\n\t\tALL contact list has been deleted "<<endl;
    }
}
void menu ()
{
    cout<<"Enter 1 to add contact "<<endl;
    cout<<"Enter 2 to display all contact "<<endl;
    cout<<"Enter 3 to search contact "<<endl;
    cout<<"Enter 4 to clear All record "<<endl;
}
int main ()
{
    int op;
    while (true )
    {
        menu();
        cin>>op;
        switch (op)
        {
        case 1:
            C_node();
            break;
        case 2:
            len = 0;
            display();
            break;
        case 3:
            search_contact_delete();
            break;

        case 4:
            clear_all();
            break;
        default:
            cout<<"Invalid Option "<<endl;
        }
    }
}