//
//
// write by kyoung chip ,jang
//
//
// g++ -o shmwriter shmwriter.cpp -fpermissive 
// ./shmwriter
//
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>
#include <string>

using namespace std; 

class CSharedMemroy
{

private :
   
    int m_shmid;    
    key_t m_key;
    char *m_shared_memory;


public :
    void setShmId( int key );
    int getShmId();

    void setKey( key_t key );

    void setupSharedMemory( int size );
    void attachSharedMemory();
    void copyToSharedMemroy( string str );
    void close();
};


void CSharedMemroy::setShmId( int id )
{
    m_shmid = id;
}


void CSharedMemroy::setKey( key_t key )
{
    m_key = key;
}


void CSharedMemroy::setupSharedMemory( int size )
{
   // Setup shared memory, 11 is the size

   if ( ( m_shmid = shmget(m_key, size , IPC_CREAT | 0666)) < 0 )
   {
      printf("Error getting shared memory id");
      exit( 1 );
   }
}


void CSharedMemroy::attachSharedMemory()
{
   // Attached shared memory
   if ( ( m_shared_memory = shmat( m_shmid , NULL , 0 ) ) == (char *)-1)
   {
      printf("Error attaching shared memory id");
      exit(1);
   }
}


void CSharedMemroy::copyToSharedMemroy( string str )
{
   // copy string to shared memory
   memcpy( m_shared_memory, str.c_str() , str.size() );
   sleep( 10 );
}

void CSharedMemroy::close()
{
   sleep(10);

   // Detach and remove shared memory
   shmdt( m_shmid );
   shmctl( m_shmid , IPC_RMID, NULL );

}


int main(int argc, const char **argv)
{
    CSharedMemroy m;

    m.setKey(777);
    m.setupSharedMemory(11);
    m.attachSharedMemory();

    m.copyToSharedMemroy("hello world");
    m.close();
}
