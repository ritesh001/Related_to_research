program band
INTEGER nkp, nband, junk, n
real  T, dist
real, allocatable:: energy(:,:)
real, allocatable:: kpoint(:,:)
real, allocatable:: kptdist(:)
real, allocatable:: temp (:,:)  !to store col 1
real, allocatable:: enband(:,:) ! to store energy of each kpoints
real, allocatable:: energyt(:,:) ! transpose of enband
open(10,file="EIGENVAL")
open(11,file="BAND")
do i = 1,5
read(10,*) 
enddo
read(10,*) junk, nkp, nband
allocate(kpoint(nkp,3))
allocate(kptdist(nkp))
allocate(temp(nband,nkp))
allocate (enband(nband,nkp))
allocate (energyt(nkp,nband)) 
do i = 1,nkp
read(10,*) kpoint(i,1), kpoint(i,2), kpoint(i,3)  ! reading kpoints
!dist= sqrt((kpoint(i,1)-kpoint(1,1))**2 +(kpoint(i,2)-kpoint(1,2))**2 +(kpoint(i,3)-kpoint(1,3))**2) ! distance from kpt1
if (i==1) then
 kptdist(i) = 0.000
else
 dist= sqrt((kpoint(i,1)-kpoint(i-1,1))**2 +(kpoint(i,2)-kpoint(i-1,2))**2 +(kpoint(i,3)-kpoint(i-1,3))**2) ! distance from kpt1
 kptdist(i)= kptdist(i-1) + dist
endif
do j = 1, nband
read(10,*)  temp(j,i), enband(j,i)   !temp(j+ (i-1)*nband), enband(j) 
enddo
!do j = 1, nband
!energyt(i,j)= enband(j,i) ! transposing enband 
  ! transposing enband 
!enddo
!read(10,*)
enddo
do i=1,nkp
write(11,*) kptdist(i), (enband(j,i), j= 1, nband)
enddo
 close(11)
 close(10)
end
