program band
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! To extract band structure from EIGENVAL                       !
! Input --> EIGENVAL output ---> BAND.dat                       !
! Copyright Swastibrata Bhattacharyya                           !
! Originally written on 11 Feb 2011                             !
! Compile gfortran -o band.out code_band_plot.f90               !
! run ./band.out                                                !
! Plot BAND.dat in any software                                 !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
INTEGER nkp, nband, junk, n, nnn1
real  T, dist, enb, efermi, j2, j3
real, allocatable:: energy(:,:)
real, allocatable:: kpoint(:,:)
real, allocatable:: kptdist(:)
real, allocatable:: temp (:,:)  !to store col 1
real, allocatable:: enband(:,:) ! to store energy of each kpoints
real, allocatable:: energyt(:,:) ! transpose of enband
open(10,file="EIGENVAL")
open(11,file="BAND.dat")
open(22,file="DOSCAR")
do i = 1,5
read(10,*)
read(22,*)
enddo
read(10,*) junk, nkp, nband
read(22,*) j2,j3,nnn1, efermi
write(*,*) efermi , nband
allocate(kpoint(nkp,3))
allocate(kptdist(nkp))
allocate(temp(nband,nkp))
allocate (enband(nband,nkp))
allocate (energyt(nkp,nband))
do i = 1,nkp
read(10,*) kpoint(i,1), kpoint(i,2), kpoint(i,3)  ! reading kpoints
do j = 1, nband
read(10,*)  temp(j,i), enb   !temp(j+ (i-1)*nband), enband(j)
enband(j,i) = enb - efermi
enddo
enddo
do i=1,nkp
!write(11,*) kptdist(i), (enband(j,i), j= 1, nband)
!write(11,*) kpoint(i,1), kpoint(i,2), (enband(j,i), j= 1, nband)
!write(11,*) kpoint(i,1), kpoint(i,2), (enband(j,i), j= 4, 5)
write(11,*) kpoint(i,1), kpoint(i,2), (enband(j,i), j= 1, nband)
enddo
 close(11)
 close(10)
end
