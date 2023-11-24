
#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <windows.h>
#include <string.h>
struct room
{
    char name[40];
    int age;
    char roomtype[40];
    int m;
} e;
//modified code
int recsize=sizeof(struct room);
char roomname[40];

//recsize = sizeof(e);

struct food
{
    char name[50];
    int price, no;
} b;

struct order
{
    char item[50], name1[50], name2[50];
    int quantity;
    double total, amount;
} l;

void view1();
void view2();
void book();
void change();
void cancel();
void menu();
void order();
void admin();
void customber();
void mainscreen();
void lodge();
void restraunt();
void addItem();

void main()
{
    printf("welcome");

    mainscreen();
}

void mainscreen()
{

    system("cls");
    int dow;
    do
    {
        printf("\033[0;36m");
        printf("\t\t*************************************************************\n");
	    printf("\t\t*                                                           *\n");
	    printf("\t\t*       -----------------------------------------           *\n");
	    printf("\t\t*        WELCOME TO RESTAURANT MANAGEMENT SYSTEM            *\n");
	    printf("\t\t*       -----------------------------------------           *\n");
	    printf("\t\t*                                                           *\n");
	    printf("\t\t*                                                           *\n");
	    printf("\t\t*                                                           *\n");
	    printf("\t\t*************************************************************\n\n\n");

        printf("\033[0m");
        printf("             Please Login:\n\n");

        printf("            1. Admin Login \n");

        printf("            2. Customer Login  \n");

        printf("            3. Exit \n\n");
        printf("\033[0;32m");
        printf("           ====================================================================\n");
        printf("            Please Select a option :");

        scanf("%d", &dow);
        printf("\033[0m");
        switch (dow)
        {
        case 1:

            admin();
            break;
        case 2:
            customber();
            break;
        case 3:
            printf("\033[0;32m");
            printf("\nVisit Again!\n\n");
            printf("\033[0m");
            exit(0);
            break;
        default:
            printf("\n Select a valid Option");
            break;
        }

    } while (dow != 4);
}

void admin()
{
    system("cls");
    char password[] = "login", p[100], ad;
passwords:
{
    printf("\n\nEnter Password:");



int ps=0;
    do{
        p[ps]=getch();
        if(p[ps]!='\r'){
            printf("*");
        }
        ps++;
    }while(p[ps-1]!='\r');
    p[ps-1]='\0';





    if (strcmp(p, password) == 0)
    {
        do
        {

            system("cls");
            printf("\033[0;36m");
            printf("\n\n\n");
            printf("\t\t        ||-----------------------------------------||           \n");
	        printf("\t\t        ||              ADMIN SECTION              ||           \n");
	        printf("\t\t        ||-----------------------------------------||           \n\n\n");
            printf("           Please select an option:\n\n");

            printf("           1. View Room Booking          \n");

            printf("           2. View Food orders           \n");

            printf("           3. Log out                  \n\n");
            printf("         ===============================================================\n\n");
            printf("            What would you like to do? ");
            scanf("%d", &ad);
            switch (ad)
            {
            case 1:
                view1();
                break;

            case 2:
                view2();

                break;

            case 3:
                mainscreen();
                break;
            default:
                printf("\n Select a valid Option");
                break;
            }

        } while (ad != 4);
    }
    else
    {
        printf("\033[0;31m");
        printf("Invalid Password!!!");
        printf("\033[0m");
        goto passwords;
    }
}
}

void customber()
{
    system("cls");
    printf("\033[0;36m");
    char cus;
    do
    {

    printf("\n                       |||||||||||||||||||||||||||||||||||||");
    printf("\n                       ||                                 ||");
    printf("\n                       ||     ***********************     ||");
    printf("\n                       ||     *                     *     ||");
    printf("\n                       ||     *       WELCOME       *     ||");
    printf("\n                       ||     *                     *     ||");
    printf("\n                       ||     ***********************     ||");
    printf("\n                       ||                                 ||");
    printf("\n                       |||||||||||||||||||||||||||||||||||||\n\n\n\n");
        printf("                    Please select an option:\n\n");

        printf("                    1. Lodging Section \n");

        printf("                    2. Restraurant Section \n");

        printf("                    3. Log out \n\n");
        printf("==============================================================================\n\n");
        printf("                    What would you like to do? ");
        scanf("%d", &cus);
        switch (cus)
        {
        case 1:
            lodge();
            break;

        case 2:
            restraunt();

            break;
        case 3:
            mainscreen();
            break;
        default:
            printf("\n Select a valid Option");
            break;
        }
    } while (cus != 4);
}

void lodge()
{
    system("cls");
    char resto;
    do
    {
        system("cls");
        printf("\t\t        ||-----------------------------------------||           \n");
	    printf("\t\t        ||              ROOM BOOKING               ||           \n");
	    printf("\t\t        ||-----------------------------------------||           \n\n\n");
        printf("           Please select an option:\n\n");

        printf("            1. Book a Room \n");

        printf("            2. View Booked Rooms \n");

        printf("            3. Change room \n");

        printf("            4. Cancel Booking \n");

        printf("            5. Go Back \n\n");
         printf("==============================================================================\n\n");
        printf("            What would you like to do? ");
        scanf("%d", &resto);
        switch (resto)
        {
        case 1:
            book();
            break;

        case 2:
            view1();
            break;

        case 3:
            change();
            break;

        case 4:
            cancel();
            break;

        case 5:
            customber();
            break;

        default:
            printf("\n Select a valid Option");
            break;
        }

    } while (resto != 6);
}

void view1()
{
    FILE *fp;
    fp = fopen("room.dat", "r");
    if (fp == NULL)
    {
        printf("file does not found !");
        exit(1);
    }
    else
    {
        printf("\n view1");
        system("cls");
        rewind(fp);
        while (fread(&e, recsize, 1, fp) == 1)
        {
            printf("\nRoom Details are: \n Name:%s Room no.:%d Age:%d Room type:%s", e.name, e.m, e.age, e.roomtype);
        }
        getch();
    }
    fclose(fp);
}

void view2()
{
    system("cls");
    char ck;
    FILE *fm;

    fm = fopen("order.dat", "r");
    if (fm == NULL)
    {
        printf("file does not found !");
        exit(1);
    }
    else
    {
        system("cls");
        if ((ck = fgetc(fm)) != EOF)
        {
            printf("\n\n");
            printf("                ||======================== OLD ORDERS ========================||\n\n");

            do
            {
                printf("%c", ck);
            } while ((ck = fgetc(fm)) != EOF);
        }
        else
            printf("No transactions");
    }
    getch();
    fclose(fm);
}

void book()
{
	//modidified code starts
	int i,j;
	//modidified code ends
    FILE *fp;
    char another, type1[] = "single", type2[] = "double";
    int g, t1, t2;
    fp = fopen("room.dat", "rb+");
    if (fp == NULL)
    {
        fp = fopen("room.dat", "wb+");
        if (fp == NULL)
        {
            printf("Cannot open file");

            exit(1);
        }
    }
    fseek(fp, 0, SEEK_END);

    another = 'y';
    while (another == 'y')
    {
        printf("\nEnter Your Details:\n");

    namer:
        printf("\nEnter your first name:");
        scanf("%s", e.name);

        for ( i = 0; i < strlen(e.name); i++)
        {
             j = e.name[i];
            if ((j >= 97 && j <= 122) || (j >= 65 && j <= 90) || (j == 32 && j == 92))
            {

                continue;
            }
            else
            {
                printf("\033[0;31m");
                printf("\nInvalid Name!");
                printf("\033[0m");
                goto namer;
            }
        }

    age:
        printf("\nEnter age: ");
        scanf("%d", &e.age);
        if (e.age <= 0)
        {
            printf("\033[0;31m");
            printf("\nInvalid age!!!\n");
            printf("\033[0m");
            goto age;
        }
        if (e.age > 120)
        {
            printf("\033[0;31m");
            printf("\nInvalid age!!!\n");
            printf("\033[0m");
            goto age;
        }
    roomf:
        printf("\nEnter Room Type (single or Double): ");
        scanf("%s", &e.roomtype);
        t1 = (strcmp(e.roomtype, type1));
        t2 = (strcmp(e.roomtype, type2));

        if (t1 == 0 || t2 == 0)
        {
            printf(" ");

        }

        else
        {
            printf("\033[0;31m");
            printf("\nInvalid room type!!!\n");
            printf("\033[0m");
            goto roomf;
        }

        g = rand() % 20;
        printf("\033[0;32m");
        printf("\n Room Booking Successful!!! \n Your room number is:%d", g);
        printf("\033[0m");

        e.m = g;

        fwrite(&e, recsize, 1, fp);

        printf("\nWould you like to Book Another Room?(y/n) ");
        fflush(stdin);
        another = getche();
    }
    fclose(fp);
}

void cancel()
{
    FILE *fp, *ft;
    char another1;
    int g;
    fp = fopen("room.dat", "rb+");
    if (fp == NULL)
    {
        fp = fopen("room.dat", "wb+");
        if (fp == NULL)
        {
            printf("Cannot open file");

            exit(1);
        }
    }
    system("cls");
    another1 = 'y';
    while (another1 == 'y')
    {
        printf("\nEnter name of name to cancel: ");
        scanf("%s", roomname);
        ft = fopen("Temp.dat", "wb");
        rewind(fp);
        while (fread(&e, recsize, 1, fp) == 1)
        {
            if (strcmp(e.name, roomname) != 0)
            {
                fwrite(&e, recsize, 1, ft);
            }
        }
        fclose(fp);
        fclose(ft);
        remove("room.dat");
        rename("Temp.dat", "room.dat");
        fp = fopen("room.dat", "rb+");
        printf("Delete another record(y/n)");
        fflush(stdin);
        another1 = getche();
    }

    fclose(fp);
}

void change()
{

    FILE *fp;
    char another2;

    fp = fopen("room.dat", "rb+");
    if (fp == NULL)
    {
        fp = fopen("room.dat", "wb+");
        if (fp == NULL)
        {
            printf("Cannot open file");

            exit(1);
        }
    }
    system("cls");
    another2 = 'y';
    while (another2 == 'y')
    {
        printf("Enter the name to change: ");
        scanf("%s", roomname);
        rewind(fp);
        while (fread(&e, recsize, 1, fp) == 1)
        {
            if (strcmp(e.name, roomname) == 0)
            {
                printf("\nEnter new name,age and room type: ");
                scanf("%s%d%s", e.name, &e.age, &e.roomtype);
                fseek(fp, -recsize, SEEK_CUR);
                fwrite(&e, recsize, 1, fp);
                break;
            }
        }
        printf("\nModify another record(y/n)");
        fflush(stdin);
        another2 = getche();
    }
    fclose(fp);
}

void menu()
{
    system("cls");
    printf("\033[0;32m");
    printf("\n\n");
    printf("                |-------------------------------------------------------|\n");
    printf("                |:::::::::::::::::::::::::MENU::::::::::::::::::::::::::|\n");
    printf("                |-------------------------------------------------------|\n");

    printf("                | ITEM NO.  ITEM                        PRICE           |\n");

    printf("                |-------------------------------------------------------|\n");
    printf("                | Item[1]   Buffalo Wings		      Rs.100        <===|\n");
    printf("                | Item[2]   Ham Burger  		      Rs.150        <===|\n");
    printf("                | Item[3]   Italian Sandwich	      Rs.60         <===|\n");
    printf("                | Item[4]   Cheese Nuggets		      Rs.100        <===|\n");
    printf("                | Item[5]   Veggie Supreme		      Rs.200        <===|\n");
    printf("                |-------------------------------------------------------|\n");
    printf("\033[0m");
    getch();
}
void order()
{
	int i,j;
    FILE *fm;
    struct order l;
    char choice1 = 'Y';

    int order = 1;
    int k;

    int num1 = 0, num2 = 0, num3 = 0, num4 = 0, num5 = 0;
    int num_customers;
    int sentinel = 0;
    const double UnitPrice1 = 100, UnitPrice2 = 150, UnitPrice3 = 60, UnitPrice4 = 100, UnitPrice5 = 200;
    double AmountofSale1 = 0, AmountofSale2 = 0, AmountofSale3 = 0, AmountofSale4 = 0, AmountofSale5 = 0, Totalsale = 0;
    system("cls");
    printf("\n\n\n");
    printf("                             ||:::::::::::::::::::MENU:::::::::::::::::::||\n\n");
    printf("\n                              Item[1] Buffalo Wings       Rs.100 <===\n");
    printf("                             ||..........................................||\n");
    printf("\n                              Item[2] Ham Burger          Rs.150 <===\n");
    printf("                             ||..........................................||\n");
    printf("\n                              Item[3] Italian Sandwich    Rs.60 <===\n");
    printf("                             ||..........................................||\n");
    printf("\n                              Item[4] Cheese Nuggets      Rs.100 <===\n");
    printf("                             ||..........................................||\n");
    printf("\n                              Item[5] Veggie Supreme      Rs.200 <===\n");
    printf("                             ||..........................................||\n\n\n");
    printf("              ==========================================================================\n\n");
    printf("\n                  Press[6] to Go back\n");

name:
    printf("\nEnter your first name:");
    scanf("%s", l.name1);
    printf("\nEnter your last name:");
    scanf("%s", l.name2);

    for ( i = 0; i < strlen(l.name1); i++)
    {
         j = l.name1[i];
        if ((j >= 97 && j <= 122) || (j >= 65 && j <= 90) || (j == 32 && j == 92))
        {

            continue;
        }
        else
        {
            printf("\033[0;31m");
            printf("\nFirst name is invalid! Enter alphabets only!!!");
            printf("\033[0m");
            goto name;
        }
    }
    for ( i = 0; i < strlen(l.name2); i++)
    {
        k = l.name2[i];
        if ((k >= 97 && k <= 122) || (k >= 65 && k <= 90) || (k == 32 && k == 92))
        {
            continue;
        }
        else
        {
            printf("\033[0;31m");
            printf("\nLast name invalid! Enter alphabets only!!!");
            printf("\033[0m");
            goto name;
        }
    }

    printf("\nFrom The List Of Food Items, What Would You Like?:\n");
    scanf("%d", &order);
    switch (order)
    {

    case 0:
        break;

    case 1:
        strcpy(l.item, "Buffalo_Wings");
        printf("\nHow Many Buffalo Wings Would You Like To Order:\n");
        scanf("%d", &num1);
        l.quantity = num1;
        AmountofSale1 = UnitPrice1 * num1;
        l.amount = UnitPrice1;
        l.total = AmountofSale1;
        break;

    case 2:

        strcpy(l.item, "Ham_Burgers");
        printf("\nHow Many Ham Burgers Would You Like To Order:\n");
        scanf("%d", &num2);
        l.quantity = num2;

        AmountofSale2 = UnitPrice2 * num2;
        l.amount = UnitPrice2;
        l.total = AmountofSale2;
        break;

    case 3:
        strcpy(l.item, "Italian_Sandwiches");
        printf("\nHow Many Italian Sandwiches Would You Like To Order:\n");
        scanf("%d", &num3);
        l.quantity = num3;

        AmountofSale3 = UnitPrice3 * num3;
        l.amount = UnitPrice3;
        l.total = AmountofSale3;
        break;

    case 4:
        strcpy(l.item, "Cheese_Nuggets");
        printf("\nHow Many Cheese Nuggets Would You Like To Order:\n");
        scanf("%d", &num4);
        l.quantity = num4;

        AmountofSale4 = UnitPrice4 * num4;
        l.amount = UnitPrice4;
        l.total = AmountofSale4;
        break;

    case 5:
        strcpy(l.item, "Veggie Supremes");
        printf("\nHow Many Would Veggie Supremes You Like To Order:\n");
        scanf("%d", &num5);
        l.quantity = num5;

        AmountofSale5 = UnitPrice5 * num5;
        l.amount = UnitPrice5;
        l.total = AmountofSale5;
        break;

    case 6:
        restraunt();
        break;

    default:
        printf("Please Choose A Valid Item From Our List\n");
    }

    fm = fopen("order.dat", "a+");

    if (fm == NULL)
    {
        printf("File not Found");
    }
    else
    {
        fprintf(fm, " \nName:%s %s  \nItem:%s  \nQuantity:%d  \nprice:Rs.%.2f \ntotal:Rs.%.2f", l.name1, l.name2, l.item, l.quantity, l.amount, l.total);
        fputs("\n", fm);
    }
    printf("-------------------------------------------------------------------------------------------------------\n");
    fclose(fm);

    Totalsale = AmountofSale1 + AmountofSale2 + AmountofSale3 + AmountofSale4 + AmountofSale5;
    {
        printf("You Have Ordered:\n\n");
        printf("===========================================================\n");

        printf("ITEM              QUANTITY     UNIT PRICE     AMOUNT OF SALE\n");

        printf("===========================================================");

        printf("\nBuffalo Wings:       %d            %.2f           %.2f  \n", num1, UnitPrice1, AmountofSale1);

        printf("\nHam Burger:          %d            %.2f           %.2f  \n", num2, UnitPrice2, AmountofSale2);

        printf("Italian Sandwich:    %d            %.2f           %.2f  \n", num3, UnitPrice3, AmountofSale3);

        printf("Cheese Nuggets:      %d            %.2f           %.2f  \n", num4, UnitPrice4, AmountofSale4);

        printf("Veggie Supreme:      %d            %.2f           %.2f  \n", num5, UnitPrice5, AmountofSale5);
    }
}
void restraunt()
{

    char dine;
    do
    {
        system("cls");
        printf("\n\n");
        printf("             **********************************\n");
        printf("             ------------ORDER FOOD------------\n");
        printf("             **********************************\n\n");
        printf("             Please select an option:\n\n");

        printf("           1. View Menu \n");

        printf("           2. Order food \n");

        printf("           3. View order \n");

        printf("           4. Go Back \n\n");
         printf("==============================================================================\n\n");
        printf("            What would you like to do? ");
        scanf("%d", &dine);
        switch (dine)
        {
        case 1:
            menu();
            break;

        case 2:
            order();
            break;

        case 3:
            view2();
            break;

        case 4:
            customber();
            break;

        default:
            printf("\n Select a valid Option");
            break;
        }

    } while (dine != 5);
}
