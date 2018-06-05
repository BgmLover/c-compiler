int fact(int i){
    if(i==1){
        return i;
    }
    else
        return i*fact(i-1);
}
int main(){
    int j;
    j=fact(4);
    return j;
}

